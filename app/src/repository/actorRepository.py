from pymongo import collection
from bson import ObjectId
from entity import Actor

class ActorRepository:

    __collection : collection.Collection

    def __init__(self, collection : collection.Collection) -> None:
        self.__collection = collection

    def insert(self, actor: Actor) -> None:
        self.__collection.insert_one(actor.toDict())

    def remove(self, id: str) -> None:
        self.__collection.delete_one({'_id': ObjectId(id)})

    def update(self, id: str, actor: Actor) -> None:
        self.__collection.update_one({'_id': ObjectId(id)}, actor.toDict())

    def findById(self, id: str) -> Actor:
        return self.__collection.find_one({'_id' : ObjectId(id)})
    
    def findManyByIds(self, ids) -> list[Actor]:
        return self.__collection.find({'_id': { '$in': ids }})

    def findAll(self) -> list[Actor]:
        return [actor for actor in self.__collection.find()]
