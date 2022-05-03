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
    async def __init__(self, database, collection):
        self.database = database
        self.collection = collection
""" 
This includes all the functions that messes with the Redemptions database. Used by the Redemption List Manager.
"""
async def ConnectDB(database):
    client = mongo.MongoClient('mongodb://localhost:27017')
    db = client[database]
    return db
async def find_one(database, collection, reqData):
    db = await ConnectDB(database)
    col = db[collection]
    return col.find_one(reqData)

async def insert_one(database, collection, dataTable):
    db = await ConnectDB(database)
    col = db[collection]
    result = col.insert_one(dataTable)
    await log("Entry <{0}> sent to collection <{1}> in database <{2}>".format(result.inserted_id, collection, database), 0)

async def get_last_inserted(database, collection):
    db = await ConnectDB(database)
    col = db[collection]
    try:
        return col.find({}).sort("InternalID", mongo.DESCENDING).limit(1).next() #This is the most complicated. It finds anything, with ASCENDING sort, limit it to the first one and selects it.]
    except StopIteration:
        await log("The collection is empty.", 3)

async def get_collection_count(database, collection):
    db = await ConnectDB(database)
    col = db[collection]
    return col.count_documents({})

async def bRedeemExist(database, collection, key, value):
    db = await ConnectDB(database)
    col = db[collection]
    try:
        dataFound = col.find({key: value}).limit(1).next()
        if len(dataFound) > 0:
            return True
        else:
            return False
    except StopIteration:
        return False

#Checks if Data already exists in Database
async def _DATAEXIST(database, collection, inputData):
    if await find_one(database, collection, inputData) == None:
        return False
    else:
        return True


if __name__ == "__main__":
    asyncio.run(log("Do not run this file directly. It's a library", 4)) #Bruh
    

