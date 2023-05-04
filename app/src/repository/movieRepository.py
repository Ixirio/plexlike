from pymongo import collection
from bson import ObjectId
from entity import Movie

class MovieRepository:

    __collection : collection.Collection

    def __init__(self, collection : collection.Collection) -> None:
        self.__collection = collection

    def insert(self, movie: Movie) -> None:
        self.__collection.insert_one(movie.toDict())

    def remove(self, id: str) -> None:
        self.__collection.delete_one({'_id': ObjectId(id)})

    def update(self, id: str, movie: Movie) -> None:
        self.__collection.update_one({'_id': ObjectId(id)}, movie.toDict())

    def findById(self, id: str) -> Movie:
        return self.__collection.find_one({'_id' : ObjectId(id)})

    def findAll(self) -> list[Movie]:
        return [movie for movie in self.__collection.find()]
