from utils.text_generation import generate


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
        self.actions = ["look", "talk", "ask"]

    def __repr__(self):
        return f"{self.type}({self.name}, {self.description}, {self.location})"

    def chooseAction(self):
        """
        Prompts the player to choose an action.
        """
        print("What would you like to do?")
        for action in self.actions:
            print(action)
        action = input(">")
        return action

    def executeAction(self, action, npcs, locations):
        """
        Executes the player's action.
        """
        if action == "look":
            self.look(locations)
        elif action == "talk":
            self.talk(npcs)
        elif action == "ask":
            self.ask()
        else:
            print("Invalid action.")

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
            print(text)

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

    def talk(self, npcs):
        """
        Prompts the player to choose a character to talk to.
        """
        conversation_history = []

        print("Who would you like to talk to?")
        for key in npcs:
            npc = npcs[key]
            if npc.location == self.location:
                print(npc.name)
        character = input("Enter Name >").strip()
        npc_selected = npcs[character]
        while True:
            dialogue = input("chat>").strip()
            if dialogue == "quit":
                npc_selected.updateMemory(self, conversation_history)
                break
            response = npc_selected.chat(dialogue, self, conversation_history)
            print(response)

            conversation_history.append(dialogue)
            conversation_history.append(response)
