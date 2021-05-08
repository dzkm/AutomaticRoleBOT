import pymongo as mongo
from pprint import pprint
from logHandler import log
import asyncio

""" 
This defines all the Database settings
TODO:
- Make a configuration screen/file for this.
"""
class dbSettings():
    async def __init__(self, database):
        self.database = database
""" 
This includes all the functions that messes with the Redemptions database. Used by the Redemption List Manager.
"""
class Database():
    async def ConnectDB(database):
        client = mongo.MongoClient('mongodb://localhost:27017')
        db = client[database]
        return db
    async def find_one(database, collection, reqData):
        db = await Database.ConnectDB(database)
        col = db[collection]
        return col.find_one(reqData)
    async def insert_one(database, collection, dataTable):
        db = await Database.ConnectDB(database)
        col = db[collection]
        result = col.insert_one(dataTable)
        log("Redeem entry with ID {0} succefully sent".format(result.inserted_id), 0)
    async def get_last_inserted(database, collection):
        db = await Database.ConnectDB(database)
        col = db[collection]
        try:
            return col.find({}).sort("InternalID", mongo.ASCENDING).limit(1).next() #This is the most complicated. It finds anything, with ASCENDING sort, limit it to the first one and selects it.]
        except StopIteration:
            log("The collection is empty.", 3)
    async def get_collection_count(database, collection):
        db = await Database.ConnectDB(database)
        col = db[collection]
        return col.count_documents({})

if __name__ == "__main__":
    log("Do not run this file directly. It's a library", 4) #Bruh
    
