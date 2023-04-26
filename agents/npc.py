from utils.text_generation import generate


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
        memory=list(),
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

    def respond(self, conversation) -> str:
        """
        Generates a response to the player's action.

        Parameters:
        -----------
        players : list
            A list of Player objects in the simulation.

        Returns:
        --------
        response : str
            The response to the player's action.
        """

        prompt = f"""
        You are {self.name}.
        You are a {self.occupation}.
        You are currently in {self.location}.
        You are {self.race}, {self.sex}, {self.age} describes as {self.description}.
        You are {self.alignment}.
        You are {self.friendliness} friendly.
        You know the following about people: {self.memory}.
        You can interact with them.

        This is the dialogue history: {conversation}.
        What is your response?
        """

        response = generate(prompt)
        print(response)
        conversation.append(response)
