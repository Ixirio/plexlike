class Actor:

    def __init__(self, name: str) -> None:
        self.__name = name

    def toDict(self) -> dict[str, any]:
        return {
            'name': self.__name
        }
