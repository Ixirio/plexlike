from datetime import datetime
from bson import ObjectId

class Movie:

    __title: str
    __description: str
    __image: str
    __year: datetime
    __actors: list[ObjectId]

    def __init__(self, title: str, year: str, actors: list[ObjectId], description = '', image: str = None) -> None:
        self.__title = title
        self.__description = description
        self.__image = image
        self.__year = datetime.strptime(year, '%Y-%m-%d')
        self.__actors = actors

    def toDict(self) -> dict[str, any]:
        return {
            'title': self.__title,
            'description': self.__description,
            'image': self.__image,
            'year': self.__year,
            'actors': self.__actors,
        }
