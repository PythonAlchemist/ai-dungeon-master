from utils.text_generation import generate
from collections import defaultdict
import os
import json
from typing import Tuple
from termcolor import cprint

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class NPC:

    """
    A class representing a non-player character in the simulation.

    Attributes:
    -----------
    name : str - The name of the agent.
    type : str - The type of agent.
    race : str - Race of the agent.
    sex : str - Sex of the agent.
    age : int - The age of the agent.
    occupation : str - The occupation of the agent.
    description : str - The description of the agents appearance and personality.
    location : str - The location of the agent.
    alignment: str - The alignment of the agent.
    friendliness : int - The friendliness of the agent (1-10)
    memory : dict - A dictionary of the agent's memories keyed by the other agent's name.
    plans : list - A list of the agent's plans.
    """

    def __init__(
        self,
        name: str,
        race: str = "human",
        sex: str = "male",
        age: int = 30,
        occupation: str = "farmer",
        description: str = "",
        location: str = '',
        alignment: str = "neutral good",
        personality: str = "average",
        friendliness: int = 5,
        memory=defaultdict(list),
        plans=list(),
    ) -> None:
        self.name = name
        self.type = "NPC"
        self.race = race
        self.sex = sex
        self.age = age
        self.occupation = occupation
        self.description = description
        self.location = location
        self.alignment = alignment
        self.personality = personality
        self.friendliness = friendliness
        self.memory = memory

    def __repr__(self):
        return f"{self.type}({self.name}, {self.description}, {self.location})"

    def chat(self, player, dm) -> None:
        """Generates a chat session between the agent and the player."""

        conversation_history = []
        info = dm.getMemory()

        while True:
            dialogue = input(f"[chat:({self.name})]>")
            if dialogue == "exit":
                break

            prompt = f"""
            Task: You are roleplaying as {self.name} and you are currently in {self.location} talking to {player.name} 
            within a Dungeons and Dragons game. You will only respond to the player's dialogue and will not speak for
            {player.name}. Remeber to stay in character as {self.name} and respond as you think {self.name} would.

            Additionally the Dungeon Master has given you information that may be important to the conversation. However only 
            use this information if you think it is relevant to the conversation.

            Dungeon Master Information:
            {info}


            Your Personality:
            You are a {self.occupation}.
            You are currently in {self.location}.
            You are {self.race}, {self.sex}, {self.age} describes as {self.description}.
            You are {self.alignment}.
            You are {self.friendliness} friendly.
            You know the following about people: {self.memory}.

            Conversation History:
            {conversation_history}

            New Dialogue:
            {dialogue}
            """

            response = generate(prompt)
            cprint(f"{self.name}:{response}", "yellow")

            conversation_history.append(f"{player.name}: {dialogue}")
            conversation_history.append(f"{self.name}: {response}")

        self.updateMemory(player, conversation_history, dm)


    def updateMemory(self, player, conversation, dm) -> Tuple[str, str]:
        """Updates the agent's memory with the player's name and the conversation history."""

        prompt = f"""
        Task: Rate the importance of this conversation (1-10) between {player.name} and myself ({self.name}).
        Summarize and compress this conversation into as few tokens as possible in the following format:

        [rate] int [/rate]
        [summary] str [/summary]

        Conversation History:
        {conversation}
        """
        response: str = generate(prompt)
        rate: str = response.split("[rate]")[1].split("[/rate]")[0]
        summary: str = response.split("[summary]")[1].split("[/summary]")[0]

        print(f"Rate: {rate}")
        print(f"Summary: {summary}")

        # TODO: allow user to add more information to the summary and recalculate

        self.memory[player.name].append((rate, summary))

        # commit to long term memory
        self._writeLongTermMemory()

        # update DM memory of the NPC interaction
        dm.memory.append(summary)

        return rate, summary

    def _loadLongTermMemory(self) -> None:
        """Loads the agent's long term memory from a file."""

        try:
            with open(f"{BASE_DIR}/agents/long_term_memory/{self.name}.json", "r") as f:
                self.memory = json.load(f)
        except FileNotFoundError:
            print(f"{self.name} has no long term memory. Creating one now...")
            self._writeLongTermMemory()
            self.memory = defaultdict(list)

    def _writeLongTermMemory(self):
        """Writes the agent's long term memory to a file."""

        with open(f"{BASE_DIR}/agents/long_term_memory/{self.name}.json", "w") as f:
            json.dump(self.memory, f)
