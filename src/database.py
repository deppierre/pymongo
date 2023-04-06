from pymongo import MongoClient
from dotenv import dotenv_values

class Database:
    def __init__(self):
        config = dotenv_values("../.env")
        self.uri=config["URI"]
        self.db_name=config["DB_NAME"]

    def get_database(self, database_name=""):
        if not database_name: database_name = self.db_name
        client = MongoClient(self.uri)

        return client[database_name]
    
    def get_collection(self, collection_name=""):
        return self.get_database()[collection_name]
    
    def insert_many(self, collection_name, docs, drop=False):
        if drop: 
            self.get_collection(collection_name).drop()
            print("Info: Drop collection {}".format(collection_name))
        result = self.get_collection(collection_name).insert_many(docs)
        print("Info: Inserted {} documents".format(len(result.inserted_ids)))

    def query_find(self, collection_name, query={}, projection={}):
        return self.get_collection(collection_name).find(query, projection)

if __name__ == "__main__":
    db = Database()
    db.insert_many("test",[{"name":"test"},{"name":"test2"}])
