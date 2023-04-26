class Location:
    """
    A class to represent a location in the simulated environment.

    """

    def __init__(self, name, type, description, owner, occupants):
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
