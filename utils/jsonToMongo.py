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

Collection.drop()
      
# Inserting the loaded data in the Collection
# if JSON contains data more than one entry
# insert_many is used else inser_one is used
if isinstance(file_data, list):
    Collection.insert_many(file_data)  
else:
    Collection.insert_one(file_data)
      
# Collection.updateMany({},[{"$set":{"date":{"$dateFromString":{"dateString":"$date"}}}}])

myclient.close()
