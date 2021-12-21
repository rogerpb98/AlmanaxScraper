import pymongo
import json
from pymongo import MongoClient, InsertOne

ip = "localhost:27017"
db = "DofusData"
options = "?maxPoolSize=20"

uri = "mongodb://"+ip+"/"+db+""+options

client = pymongo.MongoClient(uri)
db = client.DofusData
collection = db.Almanax
requesting = []

with open("../data.json", "r") as data_file:
    for jsonObj in data_file:
        data = json.loads(jsonObj)
        requesting.append(InsertOne(data))

result = collection.bulk_write(requesting)
client.close()