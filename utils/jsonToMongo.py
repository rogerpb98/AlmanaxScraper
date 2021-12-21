import pymongo
import json
from pymongo import InsertOne

# Making Connection
myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/") 
   
# database 
db = myclient["Dofus"]
   
# Created or Switched to collection 

Collection = db["Almanax"]
  
# Loading or Opening the json file
with open('data.json') as file:
    file_data = json.load(file)
      
# Inserting the loaded data in the Collection
# if JSON contains data more than one entry
# insert_many is used else inser_one is used
if isinstance(file_data, list):
    Collection.insert_many(file_data)  
else:
    Collection.insert_one(file_data)

<<<<<<< HEAD
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
=======
myclient.close()
>>>>>>> 7ae74036a97a73b9c8e3f718e1ec607f250bc8af
