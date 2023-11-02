import bson
import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['ttt']
collection = db['my_test_collection']

with open('G://Dev//test_task//sample_collection.bson', 'rb') as f:
    data = bson.decode_all(f.read())
collection.insert_many(data)
