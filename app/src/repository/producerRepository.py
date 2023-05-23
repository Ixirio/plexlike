from pymongo import collection
from bson import ObjectId
from entity import Producer

class ProducerRepository:

    __collection : collection.Collection

    def __init__(self, collection : collection.Collection) -> None:
        self.__collection = collection

    def insert(self, producer: Producer) -> None:
        self.__collection.insert_one(producer.toDict())

    def remove(self, id: str) -> None:
        self.__collection.delete_one({'_id': ObjectId(id)})

    def update(self, id: str, producer: Producer) -> None:
        self.__collection.update_one({'_id': ObjectId(id)}, {'$set': producer.toDict()})

    def findById(self, id: str) -> Producer:
        return self.__collection.find_one({'_id' : ObjectId(id)})
    
    def findManyByIds(self, ids) -> list[Producer]:
        return [producer for producer in self.__collection.find({'_id': { '$in': [ObjectId(id) for id in ids] }})]

    def findAll(self) -> list[Producer]:
        return [producer for producer in self.__collection.find()]
