class Producer:

    firstName: str
    lastName: str
    image: str

    def __init__(self, firstName: str, lastName: str, image: str = '') -> None:
        self.firstName = firstName
        self.lastName = lastName
        self.image = image

    def toDict(self) -> dict[str, any]:
        return {
            'firstName': self.firstName,
            'lastName': self.lastName,
            'image': self.image
        }
