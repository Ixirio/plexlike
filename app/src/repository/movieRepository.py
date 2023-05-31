from pymongo import collection
from bson import ObjectId
from entity import Movie
from .actorRepository import ActorRepository
from .producerRepository import ProducerRepository

# MovieRepository class
class MovieRepository:

    __collection: collection.Collection
    __actorRepository: ActorRepository
    __producerRepository: ProducerRepository

    # MovieRepository constructor
    def __init__(self, collection: collection.Collection, actorRepository: ActorRepository, producerRepository: ProducerRepository) -> None:
        self.__collection = collection
        self.__actorRepository = actorRepository
        self.__producerRepository = producerRepository

    def insert(self, movie: Movie) -> None:
        self.__collection.insert_one(movie.toDict())

    def remove(self, id: str) -> None:
        self.__collection.delete_one({'_id': ObjectId(id)})

    def update(self, id: str, movie: Movie) -> None:
        self.__collection.update_one({'_id': ObjectId(id)}, {'$set': movie.toDict()})

    def findById(self, id: str, hydrateActors: bool = True, hydrateProducers: bool = True) -> Movie:
        movie = self.__collection.find_one({'_id' : ObjectId(id)})

        # actors and producers are saved only with their id in the database
        # it's needed to query it to hydrate movies with data from actors and producers
        if hydrateActors:
            movie['actors'] = self.__actorRepository.findManyByIds(movie['actors'])

        if hydrateProducers:
            movie['producers'] = self.__producerRepository.findManyByIds(movie['producers'])

        return movie

    def findAll(self, hydrateActors: bool = True, hydrateProducers: bool = True) -> list[Movie]:
        movies = [movie for movie in self.__collection.find()]

        for movie in movies:
            # actors and producers are saved only with their id in the database
            # it's needed to query it to hydrate movies with data from actors and producers
            if hydrateActors: movie['actors'] = self.__actorRepository.findManyByIds(movie['actors'])

            if hydrateProducers: movie['producers'] = self.__actorRepository.findManyByIds(movie['producers'])

        return movies
