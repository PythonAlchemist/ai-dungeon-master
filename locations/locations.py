class Location:
    """
    A class to represent a location in the simulated environment.

    Attributes:
    -----------
    name : str - The name of the location.
    type : str - The type of location.
    description : str - The description of the location.
    owner : str - The owner of the location.
    occupants : list - A list of the location's occupants.

    """

    def __init__(self, name, type, description, owner, occupants=[]):
        self.name = name
        self.type = type
        self.description = description
        self.owner = owner
        self.occupants = occupants

    def __str__(self):
        return self.name

    def describe(self):
        """
        Prints the location's description.
        """
        info = f"""
        Name: {self.name}
        Location Type: {self.type}
        Description: {self.description}
        Owner: {self.owner}
        Minimum Occupants: {self.occupants}
        """
        return info


small_town = Location(
    name="Small Town",
    type="Town",
    description="A small town with a few shops and a tavern. Bob is the mayor and owner of the tavern.",
    owner="Bob",
    occupants=["John", "Mary", "Bob", "Sally"],
)
