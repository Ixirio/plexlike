class Actor:

    __name: str
    __image: str

    def __init__(self, name: str, image: str = '') -> None:
        self.__name = name
        self.__image = image

    def toDict(self) -> dict[str, any]:
        return {
            'name': self.__name,
            'image': self.__image
        }
