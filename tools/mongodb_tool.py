from pymongo import MongoClient
class MongoDBTool:
    def __init__(self, uri: str, db_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
    
    def find(self, collection_name: str, query: dict):
        collection = self.db[collection_name]
        return list(collection.find(query))
    
    def find_one(self,collection_name: str , query: dict):
        collection = self.db[collection_name]
        return collection.find_one(query)
    
    def aggregate(self, collection_name: str, pipeline: list):
        collection = self.db[collection_name]
        return list(collection.aggregate(pipeline))

    def insert(self, collection_name: str, document: dict):
        collection = self.db[collection_name]
        result = collection.insert_one(document)
        return result.inserted_id

        