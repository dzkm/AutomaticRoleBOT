from logHandler import log
import connections


def getItemID(itemname=None, channelName=None):
    if not itemname:
        log("Item name not specified. Check your settings.ini", 4)
        return None
    if not channelName:
        log("Channel name not specified. CHeck your settings.ini", 4)
        return None
    
    jsonData = connections.userInfo.getItemStores(channelName)
    for key in jsonData[0]:
        if key['name'] == itemname:
            return key['_id']
    