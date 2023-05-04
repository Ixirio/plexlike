from pymongo import MongoClient

class Database:

    __client: MongoClient

    def __init__(self) -> None:
        self.__client = MongoClient("mongodb://plex:plex@db:27017")

    def getClient(self):
        return self.__client['plex']
