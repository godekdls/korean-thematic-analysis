from pymongo import MongoClient
from config.config import MONGODB_CONFIG
import datetime
import traceback

client = MongoClient(MONGODB_CONFIG['host'], MONGODB_CONFIG['port'])
db = client[MONGODB_CONFIG['dbname']]


def insert(collection_name, data):
    collection = db[collection_name]
    data['date'] = datetime.datetime.now()
    try:
        collection.insert(data)
    except Exception:
        # duplicated docId
        print('failed to insert document into mongo')
        print(traceback.format_exc())


# return list of dict
def find(collection_name, query, limit=1000):
    collection = db[collection_name]
    return collection.find(query).limit(limit)


def find_one(collection_name, query):
    collection = db[collection_name]
    return collection.find_one(query)


def update_one(collection_name, query, data):
    collection = db[collection_name]
    try:
        collection.update_one(query, data)
    except Exception:
        print('failed to update document into mongo')
        print(traceback.format_exc())


def close():
    client.close()
