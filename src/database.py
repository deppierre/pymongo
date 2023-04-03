from pymongo import MongoClient
from dotenv import dotenv_values

class Database:
    def __init__(self):
        config = dotenv_values("../.env")
        self.uri=config["URI"]
        self.db_name=config["DB_NAME"]

    def get_database(self, database_name=self.db_name):
        client = MongoClient(self.uri)
        return client[database_name]
    
    def get_collection(self, collection_name):
        return self.get_database()[collection_name]

if __name__ == "__main__":
    db = Database()
    print(db.get_database())
