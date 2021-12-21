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

with open(r"../data.json") as f:
    for jsonObj in f:
        myDict = json.loads(jsonObj)
        requesting.append(InsertOne(myDict))

result = collection.bulk_write(requesting)
client.close()