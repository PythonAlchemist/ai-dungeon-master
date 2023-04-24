import openai
import os
from dotenv import load_dotenv, find_dotenv
from text2speech import Voice
from stream import TextStream, VoiceObserver
from prompts.system import jailbreak
from prompts.dungeon_master import dm_init
from prompts.players import player_prompt
import streamlit as st
from streamlit_chat import message

load_dotenv(find_dotenv())

VOICE = False

# Create a TextStream instance
text_stream = TextStream()

# Create a Voice instance
voice = Voice(mute=True)

# Register the VoiceObserver with the TextStream instance
voice_observer = VoiceObserver(voice)
text_stream.register_observer(voice_observer)

# Load your OpenAI API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_response(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.8,
    )
    message = response.choices[0].message["content"].strip()
    return message


def bot_conditioning():
    conversation_history = []

    # Jailbreak layer
    conversation_history.append({"role": "system", "content": jailbreak})
    response = generate_response(conversation_history)
    text_stream.append(response)
    conversation_history.append({"role": "assistant", "content": response})

    # DM layer
    # TODO: The LLM keeps playing for the Players, Explicitly tell the DM to stop
    conversation_history.append({"role": "system", "content": dm_init})
    response = generate_response(conversation_history)
    text_stream.append(response)
    conversation_history.append({"role": "assistant", "content": response})

    # Players layer

    conversation_history.append({"role": "system", "content": player_prompt})

    return conversation_history


def send_message(selected_user, message, conversation_history=[]):
    user_input = f"[{selected_user}] {message}"
    conversation_history.append({"role": "user", "content": user_input})

    chatbot_response = generate_response(conversation_history)
    conversation_history.append({"role": "assistant", "content": chatbot_response})

    text_stream.append(chatbot_response)

    return chatbot_response


def main():
    st.title("Chat Interface")

    user_options = {"Chris": 1, "Adam": 2, "Peter": 3}
    user_colors = {0: "#FFFFFF", 1: "#FF5733", 2: "#33FFBD", 3: "#9A33FF"}
    conversation_history = bot_conditioning()

    selected_user = st.sidebar.selectbox(
        "Choose a user", options=list(user_options.keys())
    )

    user_id = user_options[selected_user]
    chat_log = []

    chat_history = st.empty()
    message_input = st.text_input("Type your message:")

    # parse DM response from conversation_history
    for message in conversation_history:
        if message["role"] == "assistant":
            chat_log.append(("DM", message["content"], user_colors[0]))

    if st.button("Send"):
        response = send_message(selected_user, message_input, conversation_history)

        chat_log.append((selected_user, message_input, user_colors[user_id]))
        chat_log.append(("DM", response, user_colors[0]))

        # Display the entire chat history
        with chat_history:
            st.markdown("---")
            for user, message, color in chat_log:
                st.markdown(
                    f'<p style="color:{color};"><b>{user}:</b> {message}</p>',
                    unsafe_allow_html=True,
                )

        message_input = ""


if __name__ == "__main__":
    main()
