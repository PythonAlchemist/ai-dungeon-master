from agents.npc import NPC
from locations.locations import Location
from players.player import Player
import yaml

# read simulation parameters from config file
with open("simulation_config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

# create a list of NPC objects from the config file
npcs = dict()
for key in config["npcs"]:
    npc = config["npcs"][key]
    npcs[npc["name"]] = NPC(**npc)


# create a list of Player objects from the config file
players = dict()
for key in config["players"]:
    player = config["players"][key]
    players[player["name"]] = Player(**player)

# create a list of Location objects from the config file
locations = dict()
for key in config["locations"]:
    location = config["locations"][key]
    locations[location["name"]] = Location(**location)

####### SIMULATION LOOP #######

# example in the form of a conversation between a player and an NPC in the same location
# the player asks the NPC to describe the location

# choose a player
player = players["Minsc"]
player.location = locations["Golden Lion"]

# reveal player's location details
while True:
    action = player.chooseAction()
    player.executeAction(action, None, None)
