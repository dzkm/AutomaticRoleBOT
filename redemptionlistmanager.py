import asyncio
import datetime
import settings.settingsHandler as cfg
import classes.helpers.api as api
import classes.helpers.database as dbredeem
import classes.dataStorage as dataStorage
import classes.helpers.connections as connections
from logHandler import log

#TODO:
#Enviar as referencias da configurações
#Separar a parte de requests em outro script
#Alterar as referencias da classe antiga para o redeeminfo
#Adicionar o script de DB em alguma pasta
class config:
    fConfig = cfg.readConfig()
    dbName = fConfig["MongoDB"]["dbName"]
    colName = fConfig["MongoDB"]["dbCol"]
    channelName = fConfig["Twitch"]["channelName"]
    redeemItemID = api.getItemID(fConfig["StreamElements"]["itemName"], channelName)



async def nextID():
    oldID = await dbredeem.get_collection_count(config.dbName, config.colName)
    newID = oldID + 1
    return newID

""" 
Extract the list using OOP. It just feels right to do so.
"""
async def ExtractList(jsonInput):
    for entry in jsonInput:
        dataStorage.redeemData.redeemid = entry["_id"]
        dataStorage.redeemData.redeemer = entry['redeemer']['username']
        dataStorage.redeemData.item = entry['item']['name']
        dataStorage.redeemData.cor = entry['input'][0]
        dataStorage.redeemData.cargo = entry['input'][1]
        dataStorage.redeemData.dataCriada = entry["createdAt"]

        try:
            dataStorage.redeemData.discorduser = entry['input'][2]
        except IndexError:
            dataStorage.redeemData.discorduser = "NONE PROVIDED (OLD ENTRY)"
        
        try:
            dataStorage.redeemData.message = entry['message']
        except KeyError:
            dataStorage.redeemData.message = "None."

        if not await dbredeem.bRedeemExist(config.dbName, config.colName, "redeemID", dataStorage.redeemData.redeemid):
            dataStorage.redeemData.currid = await nextID()
            dataList = {"InternalID": dataStorage.redeemData.currid, "redeemID": dataStorage.redeemData.redeemid, "redeemer": dataStorage.redeemData.redeemer, "item": dataStorage.redeemData.item, "cor": dataStorage.redeemData.cor, "cargo":dataStorage.redeemData.cargo, "discord": dataStorage.redeemData.discorduser, "mensagem": dataStorage.redeemData.message, "dataCriado": dataStorage.redeemData.dataCriada, "dataAdicionado": str(datetime.datetime.now())}
            await log("USER SENT TO THE DATABASE\n\tInternalID: {0}\n\tUsername:{1}\n\tDiscord Username:{2}\n\tCargo:{3}\n\tCor do Cargo:{4}\n\tReedem ID:{5}".format(dataStorage.redeemData.currid,dataStorage.redeemData.redeemer, dataStorage.redeemData.discorduser, dataStorage.redeemData.cargo, dataStorage.redeemData.cor, dataStorage.redeemData.redeemid), 1)
            await dbredeem.insert_one(config.dbName, config.colName, dataList)
        else:
            await log("Redemption with ID {0} already exists, ignoring".format(dataStorage.redeemData.redeemid), 2)
        
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
                if not await dbredeem._DATAEXIST({"redeemID": key['_id']}):
                    await log("redeemID {0} does not exists. Adding...".format(key['_id']), 5)
                    jsonKeys.append(currentKey)
                else:
                    await log("redeemID {0} exists. Skipping...".format(key['_id']))
            currentKey +=1
    #This only adds to the filteredJson list and makes sure it doesn't repeat
    for keyPos in reversed(jsonKeys):
        if jsonInput[searchKey][keyPos]['item']['_id'] == "608c882a4c7577541a456ba7":
            if not await dbredeem._DATAEXIST({"redeemID": jsonInput[searchKey][keyPos]['_id']}):
                if jsonInput[searchKey][keyPos]['_id'] != lastid:
                    filteredJson.append(jsonInput[searchKey][keyPos])
                    lastid = jsonInput[searchKey][keyPos]['_id']
                #i += 1
    #Send it to extraction
    if len(filteredJson) > 0:
        await log("Detected new request in reedems with ID {0}".format(dataStorage.redeemData.newredeemid), 1)
        await ExtractList(filteredJson)
    else:
        await log("New reedems detected, but it's not the item required", 5)

async def ProcessData():
    jsonData = await connections.userInfo.getRedemptions(config.channelName)
    jsonDocs = jsonData['docs']
    dataStorage.redeemData.newredeemid = jsonDocs[0]['_id']
    if dataStorage.redeemData.newredeemid != dataStorage.redeemData.lastredeemid:
        jsonKeys = await GetSinceLastData()
        await FilterList(jsonData,'docs', jsonKeys=jsonKeys)
    else:
        await log("Nenhum usuário novo...", 1)


async def GetSinceLastData():
    jsonData = await connections.userInfo.getRedemptions(config.channelName)
    jsonDocs = jsonData['docs']
    currentKey = 0
    jsonKeys = []

    for key in jsonDocs:
        if key['item']['_id'] == "608c882a4c7577541a456ba7":
            continue
        if key['_id'] == dataStorage.redeemData.lastredeemid:
            break
        else:
            jsonKeys.append(currentKey)
        currentKey += 1
    return jsonKeys




async def main():
    #This is the main function (duh)
    """
    This function runs indefinetly. It checks for new discord role redeems every 5 seconds
    TODO - Make it call something to add to database (DONE)
    """

    while True:
        lastInserted = await dbredeem.get_last_inserted(config.dbName, config.colName)
        if lastInserted:
            dataStorage.redeemData.lastredeemid = lastInserted['redeemID']
        else:
            dataStorage.redeemData.lastredeemid = 0
        await log("The last redeemID inserted is {0}".format(dataStorage.redeemData.lastredeemid), 5)
        await ProcessData()
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())

