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
        self.feedback: list[str] = []

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
        you can be as descriptive as you want. Each response should be of a single thought or idea and not a sequence of thoughts or events. 
        Remember to ONLY respond as the DM and not as the players.

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

        If you are not performing your responsibilities correctly, the user the provide feedback to you. 
        Do your best to follow the feedback and improve your performance moving forward.

        Feedback: {self.feedback}

        To help you here is your memory of the simulation so far in a compressed form from 
        the original text. This should help you remember important details about the campaign.

        Long Term Memory: {self.memory}

        If there is no session history open the session as a Dungeon Master would. 
        If there is session history, continue the session as a Dungeon Master would.

        Below is the session history so far:
        Session History: {self.session_history}

        Responsd to the player as the Dungeon Master would.
        """

        response = generate(prompt, max_tokens=150)

        self.session_history.append(text)
        self.session_history.append(response)

        cprint(response, "green")

        return response

    def updateFeedback(self, instructions: str) -> None:
        """Gives the DM feedback on their performance."""
        self.feedback.append(instructions)

    def updateMemory(self) -> None:
        """Extracts the value of the conversation and adds it to the agent's memory."""

        prompt = f"""
        Task: Summarize and compress this conversation as small as possible. Only retain what will have value to the DM later.
        
        Conversation History:
        {self.session_history}
        """
        response = generate(prompt)
        print(response)

        self.memory.append(response)

        # reset the session history
    
    def getMemory(self) -> str:
        """Returns the agent's memory."""

        info: str = f"""
        Main Quest Description: {self.quest['main_quest']}
        Session History: {self.session_history}
        """

        return info

    def updateSetting(self, simulation) -> None:
        """Updates the DM with the current setting of the simulation."""
        pass


