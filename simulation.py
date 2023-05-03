from agents.dm import DM
from agents.npc import NPC
from locations.locations import Location
from players.player import Player
from typing import Union, Dict, List
from termcolor import cprint
from pathlib import Path
import inquirer
import yaml
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
quest = Path(f"{BASE_DIR}/quests/golden_lion_tavern.yaml")


class Simulation:
    def __init__(self, quest: Path = quest) -> None:
        self.all_players: list[Player] = []
        self.active_player: Player = Player()
        self.all_npcs: list[NPC] = []
        self.active_npcs: list[NPC] = []
        self.all_locations: list[Location] = []
        self.active_location: Union[Location, None] = None
        self.quest: dict[str, str] = {}
        self.__readQuest(quest)
        self.__summonDM()

    def __readQuest(self, quest) -> None:
        """read quest from yaml file"""

        # read simulation parameters from config file
        with open(quest, "r") as f:
            config: dict = yaml.load(f, Loader=yaml.FullLoader)

        # load all simulation objects
        self.all_locations = [
            Location(**config["locations"][x]) for x in config["locations"]
        ]
        self.all_npcs = [NPC(**config["npcs"][x]) for x in config["npcs"]]
        self.all_players = [Player(**config["players"][x]) for x in config["players"]]

        # load simulation parameters
        self.active_location = Location(**config["locations"]["Golden Lion"])
        self.active_npcs = [NPC(**config["npcs"][x]) for x in config["npcs"]]
        self.active_player = Player(**config["players"]["Minsc"])
        self.quest = config["quest"]

    def __summonDM(self) -> None:
        """summon the dungeon master"""

        self.dm = DM(
            locations=self.all_locations,
            npcs=self.all_npcs,
            players=self.all_players,
            quest=self.quest,
        )

    def startGame(self) -> None:
        """start the simulation"""
        # Start the session
        self.dm.rolePlay(self.active_player, "Let's Begin")

    def processRound(self) -> None:
        """process a round of the simulation"""

        # update location and npc states
        self.dm.updateSetting(self)

        questions: List = [
            inquirer.List(
                "actions",
                message="What would you like to do?",
                choices=self.active_player.actions,
            )
        ]

        action: str = inquirer.prompt(questions)["actions"]  # type: ignore Enum restriction
        self.active_player.executeAction(self, action)

    # def actionSwitch(self, text: str, npcs: dict, locations: dict, dm):
    #     """parse player actions"""

    #     if text.startswith(":look"):
    #         # TODO: implement look
    #         pass
    #     elif text.startswith(":chat"):
    #         cprint("Who would you like to talk to?", "green")

    #     elif text.startswith(":ask"):
    #         pass
    #     elif text.startswith(":yield"):
    #         pass
    #     elif text.startswith(":move"):
    #         pass
    #     else:
    #         pass
