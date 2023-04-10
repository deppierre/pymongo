from pymongo import MongoClient
from dotenv import dotenv_values

def get_database(database_name=""):
    config = dotenv_values("../.env")
    uri=config["URI"]
    db_name=config["DB_NAME"]
    if not database_name: database_name = db_name
    with MongoClient(uri) as client:
        return client[database_name]

def get_collection(collection_name=""):
    if collection_name: return get_database()[collection_name]
    else: print("Error: Collection name is required")

def insert_many(collection_name, docs, drop=False):
    if drop: 
        get_collection(collection_name).drop()
        print("Info: Drop collection {}".format(collection_name))
        
    result = get_collection(collection_name).insert_many(docs)
    print("Info: Inserted {} documents".format(len(result.inserted_ids)))
def insert(collection_name, doc, replace=False, debug=False):
    if debug: print("Debug: Inserting document: {}".format(doc))
    if replace: 
        result = get_collection(collection_name).replace_one({"name":doc["name"]}, doc, upsert=True)
        if result.modified_count > 0: print("Info: Replaced {} document".format(result.modified_count))
        if result.upserted_id: print("Info: Inserted 1 document")
    else:
        result = get_collection(collection_name).insert(doc)
        print("Info: Inserted 1 document")
def query_find(collection_name="", query={}, projection={}):
    return get_collection(collection_name).find(query, projection)

def agg(collection_name="", pipeline=[]):
    return get_collection(collection_name).aggregate(pipeline)

if __name__ == "__main__":
    insert_many("test",[{"name":"test"},{"name":"test2"}])
