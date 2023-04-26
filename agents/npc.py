from utils.text_generation import generate
from collections import defaultdict
import os
import json

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
        description: str = None,
        location: str = None,
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
        self.plans = plans

    def __repr__(self):
        return f"{self.type}({self.name}, {self.description}, {self.location})"

    def chat(self, dialogue, player, conversation_history=[]) -> str:
        """Generates a chat session between the agent and the player."""

        prompt = f"""
        Task: You are roleplaying as {self.name} and you are currently in {self.location} talking to {player.name}.
        
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

        What is your response? Remember to stay in character and only respond with new conversation. 
        If you generate new places or people in your response, that are not explicitly mentioned in your memory 
        or the conversation history, mark them as new like so: [PLACE] General Store [/PLACE] or [PERSON] Old Man Jenkins [/PERSON].
        """

        response = generate(prompt)

        # TODO: Create new agents on the fly
        # check for new places or people
        # if "[PLACE]" in response:
        #     new_place = response.split("[PLACE]")[1].split("[/PLACE]")[0]
        #     self.memory.append(new_place)
        # if "[PERSON]" in response:
        #     new_person = response.split("[PERSON]")[1].split("[/PERSON]")[0]
        #     self.memory.append(new_person)

        return response

    def updateMemory(self, player, conversation) -> None:
        """Updates the agent's memory with the player's name and the conversation history."""

        prompt = f"""
        Task: Rate the importance of this conversation (1-10) between {player.name} and myself ({self.name}).
        Summarize and compress this conversation into as few tokens as possible in the following format:

        [rate] int [/rate]
        [summary] str [/summary]

        Conversation History:
        {conversation}
        """
        response = generate(prompt)
        rate = response.split("[rate]")[1].split("[/rate]")[0]
        summary = response.split("[summary]")[1].split("[/summary]")[0]

        print(f"Rate: {rate}")
        print(f"Summary: {summary}")

        self.memory[player.name].append((rate, summary))

        # commit to long term memory
        self._writeLongTermMemory()

    def _writeLongTermMemory(self):
        """Writes the agent's long term memory to a file."""

        with open(f"{BASE_DIR}/agents/long_term_memory/{self.name}.json", "w") as f:
            json.dump(self.memory, f)
