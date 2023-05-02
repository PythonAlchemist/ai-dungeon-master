from agents.dm import DM
from agents.npc import NPC
from locations.locations import Location
from players.player import Player
from termcolor import cprint
import yaml
import os
import inquirer


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Simulation:
    def __init__(
        self, dm: DM, npcs: dict, locations: dict, players: dict, quest: dict
    ) -> None:
        self.dm = dm
        self.npcs = npcs
        self.locations = locations
        self.players = players
        self.active_player = None
        self.active_npc = None
        self.active_location = None
        self.quest = quest

    def actionSwitch(self, text: str, npcs: dict, locations: dict, dm):
        """parse player actions"""

        if text.startswith(":look"):
            # TODO: implement look
            pass
        elif text.startswith(":chat"):
            cprint("Who would you like to talk to?", "green")

        elif text.startswith(":ask"):
            pass
        elif text.startswith(":yield"):
            pass
        elif text.startswith(":move"):
            pass
        else:
            pass


if __name__ == "__main__":
    # read simulation parameters from config file
    with open(f"{BASE_DIR}/quests/golden_lion_tavern.yaml", "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    # create a list of Location objects from the config file
    locations = dict()
    for key in config["locations"]:
        location = config["locations"][key]
        locations[location["name"]] = Location(**location)

    # create a list of NPC objects from the config file
    npcs = dict()
    for key in config["npcs"]:
        npc = config["npcs"][key]
        npcs[npc["name"]] = NPC(**npc)

        # set the NPC's location
        npcs[npc["name"]].location = locations[npc["location"]]

    # create a list of Player objects from the config file
    players = dict()
    for key in config["players"]:
        player = config["players"][key]
        players[player["name"]] = Player(**player)

    # quest description
    quest = config["quest"]

    # create a DM object
    dm = DM(quest=quest, locations=locations, npcs=npcs, players=players)

    # create a Simulation object
    simulation = Simulation(
        dm=dm, npcs=npcs, locations=locations, players=players, quest=quest
    )

    ####### SIMULATION LOOP #######

    # choose a player and location to start the simulation
    simulation.active_player = players["Minsc"]
    simulation.active_location = locations["Golden Lion"]
    simulation.active_npc = npcs

    questions = [
        inquirer.List(
            "actions",
            message="What would you like to do?",
            choices=simulation.active_player.actions,
        )
    ]

    while True:
        action = inquirer.prompt(questions)["actions"]
        resp = simulation.active_player.executeAction(simulation, action)
        print(resp)
