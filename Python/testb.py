# from pymongo import MongoClient
# from bson.objectid import ObjectId
# uri = "mongodb+srv://admin:aepibooth2023@booth.fvs2kjk.mongodb.net/?retryWrites=true&w=majority"
# client = MongoClient(uri)
# db = client.booth
# collection = db.rfid_mappings
# collection2 = db.users

# def get_user(rfid):
#   return collection.find_one({"rfid": rfid})

# myquery = { "username": "notDavid" }
# newvalues = { "$set": { "info.pokemon_name": "pikachu"}}

# collection2.update_one(myquery, newvalues)

# print(get_user('RANDOMTAG'))

# for i in collection2.find():
#     print(i)



import multiprocessing

def process_func():
    my_string = "Hello, world!"
    my_list = [1, 2, 3, 4, 5]
    return my_string, my_list

if __name__ == "__main__":
    p = multiprocessing.Process(target=process_func)
    p.start()
    p.join()
    result_string, result_list = p.exitcode
    print(result_string)
    print(result_list)