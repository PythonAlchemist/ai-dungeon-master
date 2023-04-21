import openai
import os
from dotenv import load_dotenv, find_dotenv
from text2speech import Voice
from stream import TextStream, VoiceObserver
from prompts.system import jailbreak
from prompts.dungeon_master import dm_init
from prompts.players import player_prompt

load_dotenv(find_dotenv())

# Create a TextStream instance
text_stream = TextStream()

# Register the VoiceObserver with the TextStream instance
voice_observer = VoiceObserver(Voice())
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


def main():
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

    while True:
        try:
            user_input = input("User: ")
            conversation_history.append({"role": "user", "content": user_input})

            chatbot_response = generate_response(conversation_history)
            conversation_history.append(
                {"role": "assistant", "content": chatbot_response}
            )

            print(f"ChatGPT: {chatbot_response}")
            text_stream.append(chatbot_response)

        except KeyboardInterrupt:
            print("\nEnding the conversation.")
            break


if __name__ == "__main__":
    main()
