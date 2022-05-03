import configparser
import asyncio

DEFAULT_CONNECTIONSTRING = "mongodb://127.0.0.1:27017"

fConfig = configparser.ConfigParser()

async def _hereConfig():
    try:
        with open('settings.ini', 'r') as file:
            file.close
        return True
    except FileNotFoundError:
        return False
    except PermissionError:
        raise("Not enough permissions to create config file. Ending program.")


async def createConfig():
    fConfig["Twitch"]={
        "channelName":"Kappa"}

    fConfig["StreamElements"]={
        "jwtToken":"<insert your token>",
        "itemName":"Discord Addon",
        "queryLimit":"500",
        "queryOffset":"0",
        "onlyPending":"True"
    }

    fConfig["MongoDB"]={
        "Host":"127.0.0.1",
        "Port":"27017",
        "dbName":"redemptions",
        "dbCol":"redeems",
        "connectionString":DEFAULT_CONNECTIONSTRING
    }

    fConfig["Advanced"]={
        "Debug":"False"
    }

    with open('settings.ini', 'w+') as fSettings:
        fConfig.write(fSettings)
        fSettings.flush()
        fSettings.close()
    
async def readConfig():
    while not await _hereConfig():
        print("Python file not here")
        await createConfig()
    fConfig.read("settings.ini")
    return fConfig

if __name__ == "__main__":
    asyncio.run(readConfig())