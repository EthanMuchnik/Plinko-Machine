from pymongo import MongoClient
from bson.objectid import ObjectId
uri = "mongodb+srv://admin:aepibooth2023@booth.fvs2kjk.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client.booth
collection = db.rfid_mappings
collection2 = db.users

def get_user(rfid):
  return collection.find_one({"rfid": rfid})

myquery = { "username": "notDavid" }
newvalues = { "$set": { "info.pokemon_name": ""}}

collection2.update_one(myquery, newvalues)

print(get_user('RANDOMTAG'))

for i in collection2.find():
    print(i)

