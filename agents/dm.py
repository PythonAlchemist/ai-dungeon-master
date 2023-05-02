from utils.text_generation import generate
import os
from termcolor import cprint
import csv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


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
        self.training_data = self.getWriter()

    def __repr__(self):
        return f"{self.type}({self.name})"

    def getWriter(self):
        """Returns a writer object for writing training data to a file."""

        # create a csv file if it doesn't exist
        if not os.path.exists(f"{BASE_DIR}/../data/dm_classifier.csv"):
            file = open(f"{BASE_DIR}/../data/dm_classifier.csv", "w")
            writer = csv.writer(file)
            writer.writerow(["text", "label"])

        # append to the csv file if it does exist
        else:
            file = open(f"{BASE_DIR}/../data/dm_classifier.csv", "a")
            writer = csv.writer(file)

        return writer

    def rolePlay(self, player, text="") -> str:
        """Generates a response to the player's text."""

        prompt = f"""
        Task: You are playing the role of the Dungeon Master for a Dungeons and Dragons game. This will be short theater of the mind style game and the primary goal is for the players 
        to have fun. You will be playing the role of the Dungeon Master and will be responsible for narrating the story and describing the environment outside of direct dialogue. Try to 
        model your performance after Matt Mercer, DM for Critical Role. Below I will provide you with context about the primary quest line and the characters you will be interacting with. 
        Your primary task is narration, you should not be creating multi response dialogue between NPCs or Players.

        Main Quest Description: {self.quest['main_quest']}
        Quest Intro: {self.quest['intro']}

        Players: {[p for p in self.players]}
        NPCs: {[p for p in self.npcs]}
        Locations: {[p for p in self.locations]}

        Your Responsibilities:
        - Keep the players and NPCs on track of the primary plot line
        - Narrate the story and describe the environment outside of direct dialogue
        - Interact with tools within the simulation to help you accomplish your goals

        UNDER NO CIRCUMSTANCES SHOULD YOU DO THE FOLLOWING OR THE SIMULATION WILL TERMINATE:
        - Speak for the players
        - Make decisions for the players

        Long Term Memory: {self.memory}

        With this information in mind, Keep answers short unless you are describing the environment or 
        being long winded for artistic effect. If there is no session history open the session as a 
        Dungeon Master would. If there is session history, continue the session as a Dungeon Master would.

        Session History: {self.session_history}
        """

        response = generate(prompt, max_tokens=150)

        self.session_history.append(f"{player}: {text}")
        self.session_history.append(f"DM: {response}")

        cprint(response, "green")

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

    # TODO: This does not work as expected.
    def informNPC(self, npc, player, location) -> str:
        """Informs the NPC of the quest details."""

        prompt = f"""
        Task: A NPC ({npc.name}) is in a conversation with a player ({player.name}) at {location}. You need to inform the NPC about anything 
        that is relevant to a quest or plot that {npc.name} would know.

        To help you here is your memory of the simulation so far:

        Long Term Memory: {self.memory}
        Session History: {self.session_history}
        """

        response = generate(prompt)
        cprint(f"VOICE: {response}", "red")

        return response
