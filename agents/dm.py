from utils.text_generation import generate
from collections import defaultdict
import os
import json
from termcolor import cprint

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class DM:

    """
    A class representing the Dungeon Master in the simulation. This agent controls the overall narrative of the simulation.

    The DM is responsible for:
    - Generating the story
    - Keeping the players and NPCs on track of the primary plot line
    - Narrating the story and describing the environment outside of direct dialogue
    - Passing pertinent information to the NPCs during conversations


    Attributes:
    -----------
    name : str - The name of the agent.
    type : str - The type of agent.

    """

    def __init__(self, locations=None, npcs=None, players=None, quest=None) -> None:
        self.name = "Dungeon Master"
        self.type = "DM"
        self.locations = locations
        self.npcs = npcs
        self.players = players
        self.quest = quest
        self.session_history = []
        self.memory = []

    def __repr__(self):
        return f"{self.type}({self.name})"

    @staticmethod
    def _clean(text):
        """Cleans the text for printing."""
        text = text.replace("\n", "")
        text = text.replace("  ", " ")
        return text

    def rolePlay(self, player, text) -> str:
        """Generates a response to the player's text."""

        prompt = f"""
        Task: You are playing the role of the Dungeon Master for a Dungeons and Dragons game. This will be short theater of the mind style game and the primary goal is for the players 
        to have fun. You will be playing the role of the Dungeon Master and will be responsible for narrating the story and describing the environment outside of direct dialogue. Try to 
        model your performance after Matt Mercer, DM for Critical Role. Below I will provide you with context about the primary quest line and the characters you will be interacting with.

        Main Quest Description: {self.quest['main_quest']}
        Quest Intro: {self.quest['intro']}

        Players: {[p for p in self.players]}
        NPCs: {[p for p in self.npcs]}
        Locations: {self.locations}

        Your Responsibilities:
        - Keep the players and NPCs on track of the primary plot line
        - Narrate the story and describe the environment outside of direct dialogue
        - Pass pertinent information to the NPCs during conversations

        UNDER NO CIRCUMSTANCES SHOULD YOU DO THE FOLLOWING OR YOU WILL BE DISQUALIFIED:
        - Speak for the players
        - Speak for the NPCs

        You can interact with other programs within this similation by typing the following commands:
            [chat: (NPC_NAME, EXTRA_INFORMATION, INITIAL_DIALOGUE)] - Start a chat session with an NPC
            NPC_NAME - The name of the NPC you want to chat with
            EXTRA_INFORMATION - Any extra information you want to provide the NPC to help guide the conversation since you the DM are all knowing
            INITIAL_DIALOGUE - The initial dialogue you want the NPC to say to the player to start the conversation if any
        
        Example:
        ====================
        Prompt (from the party): We enter the tavern and look around for a table to sit at.
        Response: 
        As you enter the tavern you see a few tables open. You also notice an elderly wizard staring at you from 
        the corner of the room. He seems to be alone and is wearing a blue robe with a pointy hat. He makes his 
        way over to you and says,

        [chat: (Gandalf, None, Hello there!)]
        ====================
        This will start a chat session with Gandalf between the players and a seperate AI agent. The summary 
        of the conversation will be passed to you and you will be responsible for noting any important from the interaction. But you 
        will NOT speak for the NPC. You will only speak for the NPC when you are narrating the story or describing the environment.

        Long Term Memory: {self.memory}

        With this information in mind, please start our session

        Session History: {self.session_history}
        """

        response = generate(prompt)

        # this doesn't work.
        # TODO: build a classifer to determine if chat needs to be started

        # start a conversation with an NPC
        if "[chat:" in response:
            before = response.split("[chat:")[0]
            chat_vals = response.split("[chat:")[1].split("]")[0]
            npc = chat_vals.split(",")[0]
            extra = chat_vals.split(",")[1]
            init = chat_vals.split(",")[2]

            cprint(before, "green")

            if npc in self.npcs.keys():
                rate, summary = self.npcs[npc].chat(player, extra, init)
            else:
                print(f"{npc} is not a valid NPC.")

        else:
            cprint(response, "green")

        if len(self.session_history) == 0:
            self.session_history.append(prompt)
        else:
            self.session_history.append(text)

        self.session_history.append(response)

        return response

    def updateMemory(self, conversation) -> None:
        """Extracts the value of the conversation and adds it to the agent's memory."""

        prompt = f"""
        Task: Summarize and compress this conversation as small as possible. Only retain what will have value to the DM later.
        
        Conversation History:
        {conversation}
        """
        response = generate(prompt)
        print(response)

        self.memory.append(response)
