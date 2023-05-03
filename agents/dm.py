from utils.text_generation import generate
import os
from termcolor import cprint
import csv
from typing import Tuple
from agents.npc import NPC
from players.player import Player
from locations.locations import Location

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

    def __init__(
        self,
        locations: list[Location],
        npcs: list[NPC],
        players: list[Player],
        quest: dict = {},
    ) -> None:
        self.locations = locations
        self.npcs = npcs
        self.players = players
        self.quest = quest
        self.name: str = "Dungeon Master"
        self.type: str = "DM"
        self.session_history: list[str] = []
        self.memory: list[Tuple[int, str]] = []

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
        to have fun. You will be playing the role of the Dungeon Master and will be responsible for narrating the story and describing the environment outside of direct dialogue. 
        Below I will provide you with context about the primary quest line and the NPCs important to this quest. 
        Your primary task is narration, keep your answers short unless you are describing the environment or a character, then 
        you can be as descriptive as you want. Each response should be of a single thought or idea and not a sequence of thoughts or events

        Main Quest Description: {self.quest['main_quest']}
        Quest Intro: {self.quest['intro']}

        NPCs: {[p.name for p in self.npcs]}
        Locations: {[p.name for p in self.locations]}

        Current Location: {player.location}

        Your Responsibilities:
        1. Keep the players and NPCs on track of the primary plot line
        2. Narrate the story and describe the environment outside of direct dialogue

        UNDER NO CIRCUMSTANCES SHOULD YOU DO THE FOLLOWING OR THE SIMULATION WILL TERMINATE:
        1. Speak for the players
        2. Make decisions for the players

        Long Term Memory: {self.memory}

        If there is no session history open the session as a Dungeon Master would. 
        If there is session history, continue the session as a Dungeon Master would.

        Session History: {self.session_history}
        """

        response = generate(prompt, max_tokens=150)

        self.session_history.append(text)
        self.session_history.append(response)

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
    def informNPC(self, npc, player, location) -> Tuple[str, str]:
        """Informs the NPC of the quest details."""

        prompt = f"""
        Task: A NPC named {npc.name} is in a conversation with a player named {player.name} at {location}. 
        You need to inform the NPC about anything that is relevant to a quest or plot that {npc.name} would know. 
        If they are not important to the quest or plot, then you do not need to inform them and respond with "None".
        If you have initiated dialogue in character of {npc.name} then response with that dialogue.

        Your response should be formatted as follows:
        [info] Anything you want the NPC to know OR None [/info]
        [dialogue] Anything the NPC has already said OR None [/dialogue]

        To help you here is your memory of the simulation so far:

        Long Term Memory: {self.memory}
        Session History: {self.session_history}
        """

        response = generate(prompt)
        cprint(f"VOICE: {response}", "red")

        # split the response into the info and dialogue
        info = response.split("[info]")[1].split("[/info]")[0]
        dialogue = response.split("[dialogue]")[1].split("[/dialogue]")[0]

        return info, dialogue
    
    def updateSetting(self, simulation) -> None:
        """Updates the DM with the current setting of the simulation."""
        pass


