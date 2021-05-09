import requests
import asyncio
import json
import datetime
from logHandler import log
from databasehandler import Database as dbredeem
from pprint import pprint
from requests.structures import CaseInsensitiveDict
from os import getcwd as CURR_DIR


dbName = 'redemptions'
colName = 'redeems'
channelName = "5a41d7a44469c70001f174fc"
urlAPI = "https://api.streamelements.com/kappa/v2/store/{0}/redemptions/?pending=true".format(channelName)

class Info:
    async def __init__(self, currid, redeemid, redeemer, cargo, cor, item, message, lastredeemid, discorduser, newredeemid):
        self.currid = currid
        self.redeemid = redeemid
        self.redeemer = redeemer
        self.cargo = cargo
        self.cor = cor
        self.item = item
        self.message = message
        self.lastredeemid = lastredeemid
        self.discorduser = discorduser
        self.newredeemid = newredeemid
    async def reqheaders():
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Content-Type"] = "text/plain"
        headers["Authorization"] = "Bearer {}".format(await GetAuthToken())
        return headers
#Gets AuthToken from token.txt
async def GetAuthToken():
    file = open(CURR_DIR() + "\Token.txt", "r")
    return file.readline().strip()

#Checks if Data already exists in Database
async def _DATAEXIST(inputData):
    if await dbredeem.find_one(dbName, colName, inputData) == None:
        return False
    else:
        return True

async def nextID():
    oldID = await dbredeem.get_collection_count(dbName, colName)
    newID = oldID + 1
    return newID

""" 
Extract the list using OOP. It just feels right to do so.
"""
async def ExtractList(jsonInput):
    for entry in jsonInput:
        Info.redeemid = entry["_id"]
        Info.redeemer = entry['redeemer']['username']
        Info.item = entry['item']['name']
        Info.cor = entry['input'][0]
        Info.cargo = entry['input'][1]
        Info.dataCriada = entry["createdAt"]

        try:
            Info.discorduser = entry['input'][2]
        except IndexError:
            Info.discorduser = "NONE PROVIDED (OLD ENTRY)"
        
        try:
            Info.message = entry['message']
        except KeyError:
            Info.message = "None."

        if not await dbredeem.bDataExist(dbName, colName, "redeemID", Info.redeemid):
            Info.currid = await nextID()
            dataList = {"InternalID": Info.currid, "redeemID": Info.redeemid, "redeemer": Info.redeemer, "item": Info.item, "cor": Info.cor, "cargo":Info.cargo, "discord": Info.discorduser, "mensagem": Info.message, "dataCriado": Info.dataCriada, "dataAdicionado": str(datetime.datetime.now())}
            await log("USER SENT TO THE DATABASE\n\tInternalID: {0}\n\tUsername:{1}\n\tDiscord Username:{2}\n\tCargo:{3}\n\tCor do Cargo:{4}\n\tReedem ID:{5}".format(Info.currid,Info.redeemer, Info.discorduser, Info.cargo, Info.cor, Info.redeemid), 1)
            await dbredeem.insert_one(dbName, colName, dataList)
        else:
            await log("Redemption with ID {0} already exists, ignoring".format(Info.redeemid), 2)
        
""" 
Filters the List to only have reedems of Discord. This works like a fucking professional piece of code.
"""
async def FilterList(jsonInput, searchKey='docs', jsonKeys=[]):
    #Sets all variables
    filteredJson = []
    i = 0
    lastid = ""
    
    if len(jsonKeys) > 0:
        _HASJSONKEYS = True
    else:
        _HASJSONKEYS = False
        await log("jsonKeys were not sent. Making hard checkup.", 3)
    
    #This method goes through all keys and filters the one with the ID provided below. Works hella fine.
    if not _HASJSONKEYS:
        currentKey = 0
        for key in jsonInput[searchKey]:
            if key['item']['_id'] == "608c882a4c7577541a456ba7":
                if not await _DATAEXIST({"redeemID": key['_id']}):
                    await log("redeemID {0} does not exists. Adding...".format(key['_id']), 5)
                    jsonKeys.append(currentKey)
                else:
                    await log("redeemID {0} exists. Skipping...".format(key['_id']))
            currentKey +=1
    #This only adds to the filteredJson list and makes sure it doesn't repeat
    for keyPos in reversed(jsonKeys):
        if jsonInput[searchKey][keyPos]['item']['_id'] == "608c882a4c7577541a456ba7":
            if jsonInput[searchKey][keyPos]['_id'] != lastid:
                filteredJson.append(jsonInput[searchKey][keyPos])
                lastid = jsonInput[searchKey][keyPos]['_id']
                #i += 1
    #Send it to extraction
    await ExtractList(filteredJson)

async def ProcessData():
    jsonData = await GetData()
    jsonDocs = jsonData['docs']
    Info.newredeemid = jsonDocs[0]['_id']
    if Info.newredeemid != Info.lastredeemid:
        await log("Detected new request in reedems with ID {0}".format(Info.newredeemid), 1)
        jsonKeys = await GetSinceLastData()
        await FilterList(jsonData,'docs', jsonKeys=jsonKeys)
    else:
        await log("Nenhum usuário novo...", 1)


async def GetSinceLastData():
    jsonData = await GetData()
    jsonDocs = jsonData['docs']
    currentKey = 0
    jsonKeys = []

    for key in jsonDocs:
        if key['_id'] == Info.lastredeemid:
            break
        else:
            jsonKeys.append(currentKey)
        currentKey += 1
    return jsonKeys


""" 
This function calls the API so we can get the json
"""
async def GetData():
    redemptionListURL = urlAPI
    request = requests.request("GET", redemptionListURL, headers=await Info.reqheaders())
    jsonfuck = json.loads(request.content)
    return jsonfuck



async def main():
    #This is the main function (duh)
    """
    This function runs indefinetly. It checks for new discord role redeems every 5 seconds
    TODO - Make it call something to add to database (DONE)
    """

    while True:
        lastInserted = await dbredeem.get_last_inserted(dbName, colName)
        if lastInserted:
            Info.lastredeemid = lastInserted['redeemID']
        else:
            Info.lastredeemid = 0
        await log("The last redeemID inserted is {0}".format(Info.lastredeemid), 5)
        await ProcessData()
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())

