from pymongo import MongoClient
from config.config import MONGODB_CONFIG
import datetime

client = MongoClient(MONGODB_CONFIG['host'], MONGODB_CONFIG['port'])
db = client[MONGODB_CONFIG['dbname']]

def insert(collection_name, data):
    collection = db[collection_name]
    data['date'] = datetime.datetime.now()
    collection.insert(data)


def close():
    client.close()
