from utils.text_generation import generate
from termcolor import cprint
import inquirer


class Player:

    """
    A class for user-controlled players to interact with the simulated environment.

    Attributes:
    -----------
    name : str - The name of the character.
    type : str - The type of the agent
    race : str - Race of the agent.
    sex : str - Sex of the agent.
    age : int - The age of the agent.
    description : str - The description of the character.
    location : str - The location of the character.
    CHARISMA : int - The character's charisma.
    actions : list - A list of the character's possible actions.
    """

    def __init__(self, name, race, sex, age, description, location, CHARISMA) -> None:
        self.name = name
        self.type = "PC"
        self.race = race
        self.sex = sex
        self.age = age
        self.description = description
        self.location = location
        self.CHARISMA = CHARISMA
        self.actions = ["look", "chat", "ask", "yield", "move"]
        self.memory = []

    def __repr__(self):
        return f"{self.type}({self.name}, {self.description}, {self.location})"

    def executeAction(self, simulation, action):
        """
        Executes the player's action.
        """
        location = simulation.active_location
        npcs = simulation.active_npc
        dm = simulation.dm

        if action == "look":
            resp = self.look(location)
        elif action == "chat":
            resp = self.chat(npcs)
        elif action == "ask":
            resp = self.ask()
        elif action == "yield":
            resp = self.yieldAction(dm)
        else:
            print("Invalid action.")

        return resp

    def ask(self, conversation_history=[]):
        """
        Ask an open ended question.
        """
        while True:
            question = input("ask>")

            prompt = f"""
            Task: A Player in a role playing game is asking to ask an open ended question.
            Respond as a Dungeon Master in a story would given the player question and context provided.
            
            Player: {question}
            Location: {self.location}
            Location Description: {self.location.describe()}
            conversation_history: {conversation_history}
            """

            text = generate(prompt)

            conversation_history.append(question)
            conversation_history.append(text)

            if question == "quit":
                break

    def look(self, locations):
        """
        Prints the description of the current location.
        """
        for location in locations:
            if location.name == self.location:
                print(location.description)

    def chat(self, npcs):
        """
        Prompts the player to choose a character to talk to.
        """
        questions = [
            inquirer.List(
                "chat options",
                message="Who would you like to chat with?",
                choices=npcs,
            )
        ]
        answers = inquirer.prompt(questions)["chat options"]
        npc_selected = npcs[answers]

        npc_selected.chat(self)

    def yieldAction(self, dm):
        """
        Yields to the DM.
        """
        resp = dm.rolePlay(self, "")
        return resp
