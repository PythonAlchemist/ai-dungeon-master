players_init = """Next we will introduce the players."""
players = [
    """
    [Vax] My name is Chris and I will be playing the role of Vax'ildan, the Goliath Barbarian. I hail from a tribe of blood thirsty warriors who live in the mountains of the Stolen Lands. 
    I am a fierce warrior who is not afraid of conflict but I still have a soft spot for my friends.
    """,
    """
    [Armedis] My name is Adam and I will be playing the role of Armedis, a Tiefling Rogue who is member of the Scarlet Brotherhood. A group of assassins who are sworn to protect the people of Baldur's Gate.
    """,
    """
    [Pimpop] I am Peter and I will be playing Pimpop, the racist gnome cleric.
    """,
]

player_prompt = players_init
for player in players:
    player_prompt += player
