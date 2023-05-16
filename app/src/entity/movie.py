from datetime import datetime
from bson import ObjectId

class Movie:

    title: str
    description: str
    image: str
    year: datetime
    actors: list[ObjectId]

    def __init__(self, title: str, year: str, actors: list[ObjectId], description = '', image: str = None) -> None:
        self.title = title
        self.description = description
        self.image = image
        self.year = datetime.strptime(year, '%Y-%m-%d')
        self.actors = actors

    def toDict(self) -> dict[str, any]:
        return {
            'title': self.title,
            'description': self.description,
            'image': self.image,
            'year': self.year,
            'actors': self.actors,
        }
