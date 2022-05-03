import requests
from requests.structures import CaseInsensitiveDict
import json

class Info:
    async def __init__(self, authToken, urlAPI):
        self.authToken = authToken
        self.urlAPI = urlAPI
    
    async def reqheaders():
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Content-Type"] = "text/plain"
        headers["Authorization"] = "Bearer {}".format(Info.authToken)
        return headers

class userInfo():
    async def getItemStores(username):
        Info.urlAPI = "https://api.streamelements.com/kappa/v2/store/{}/items".format(username)
        return getData.requestJson()

    async def getRedemptions(username):
        Info.urlAPI = "https://api.streamelements.com/kappa/v2/store/{}/redemptions/?pending=true".format(username)
        return getData.requestJson()

class getData():
    async def requestJson():
        request = requests.request("GET", Info.urlAPI, headers=await Info.reqheaders())
        jsonData = json.loads(request.content)
        return jsonData