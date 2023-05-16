from pymongo import collection
from bson import ObjectId
from entity import Movie
from .actorRepository import ActorRepository

class MovieRepository:

    __collection: collection.Collection
    __actorRepository: ActorRepository

    def __init__(self, collection: collection.Collection, actorRepository: ActorRepository) -> None:
        self.__collection = collection
        self.__actorRepository = actorRepository

    def insert(self, movie: Movie) -> None:
        self.__collection.insert_one(movie.toDict())

    def remove(self, id: str) -> None:
        self.__collection.delete_one({'_id': ObjectId(id)})

    def update(self, id: str, movie: Movie) -> None:
        self.__collection.update_one({'_id': ObjectId(id)}, {'$set': movie.toDict()})

    def findById(self, id: str, hydrateActors: bool = True) -> Movie:
        movie = self.__collection.find_one({'_id' : ObjectId(id)})

        if hydrateActors:
            movie['actors'] = self.__actorRepository.findManyByIds(movie['actors'])

        return movie

    def findAll(self, hydrateActors: bool = True) -> list[Movie]:
        movies = [movie for movie in self.__collection.find()]

        if hydrateActors:
            for movie in movies:
                movie['actors'] = self.__actorRepository.findManyByIds(movie['actors'])

        return movies
