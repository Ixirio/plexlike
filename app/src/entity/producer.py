class Producer:

    firstName: str
    lastName: str
    image: str

    # Producer entity constructor
    def __init__(self, firstName: str, lastName: str, image: str = '') -> None:
        self.firstName = firstName
        self.lastName = lastName
        self.image = image

    # Method to cast entity to a dict to store it in the mongo Database 
    def toDict(self) -> dict[str, any]:
        return {
            'firstName': self.firstName,
            'lastName': self.lastName,
            'image': self.image
        }
