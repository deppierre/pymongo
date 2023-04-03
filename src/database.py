from pymongo import MongoClient
from dotenv import dotenv_values

class Database:
    def __init__(self):
        config = dotenv_values("../.env")
        self.uri=config["URI"]
        self.db_name=config["DB_NAME"]

    def get_database(self):
        client = MongoClient(self.uri)
        return client[self.db_name]

if __name__ == "__main__":
    db = Database()
    print(db.get_database())
