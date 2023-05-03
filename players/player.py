from utils.text_generation import generate
from termcolor import cprint
import inquirer
from enum import Enum
from locations.locations import Location, small_town
from typing import Tuple, TYPE_CHECKING



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

    def __init__(
        self,
        name: str = "John",
        race: str = "Human",
        sex: str = "Male",
        age: int = 35,
        description: str = "",
        location: Location = small_town,
        CHARISMA: int = 12,
    ) -> None:
        self.name: str = name
        self.type: str = "PC"
        self.race: str = race
        self.sex: str = sex
        self.age: int = age
        self.description: str = description
        self.location: Location = location
        self.CHARISMA: int = CHARISMA
        self.actions: list[str] = ["chat", "ask", "feedback"]
        self.memory: list[Tuple[int, str]] = []

    def __repr__(self):
        return f"{self.type}({self.name}, {self.description}, {self.location})"

    def executeAction(self, simulation, action: str):
        """
        Executes the player's action.
        """

        if action == "chat":
            resp = self.chat(simulation)
        elif action == "ask":
            resp = self.ask(simulation)
        else:
            resp = "Broken"
            print("Invalid action.")

        return resp

    def ask(self, simulation):
        """
        Ask an open ended question.
        """

        dm = simulation.dm
        dialog = input("ask>")
        resp = dm.rolePlay(self, dialog)
        return resp

    def chat(self, simulation):
        """
        Prompts the player to choose a character to talk to.
        """
        dm = simulation.dm
        npcs = {npc.name: npc for npc in dm.npcs}
        questions = [
            inquirer.List(
                "chat options",
                message="Who would you like to chat with?",
                choices=[npc.name for npc in dm.npcs],
            )
        ]
        answers = inquirer.prompt(questions)["chat options"]  # type: ignore
        npc_selected = npcs[answers]

        npc_selected.chat(self, dm)

    def feedback(self, simulation):
        """
        Allows the player to provide feedback to the DM.
        """
        dm = simulation.dm
        dialog = input("feedback>")
        resp = dm.updateFeedback(self, dialog)
        print(resp)
        return resp
