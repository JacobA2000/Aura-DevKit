import json
import os

def CheckDirExistsAndCreateIfNot(path):
    #Checks if a directory exists and if not creates it.
    if os.path.exists(path):
        return True
    else:
        os.mkdir(path)
        return f"Created directory {path}."

def CheckIfConfigExists(path):
    #Checks if a directory exists.
    if os.path.exists(path):
        return True
    else:
        return False

def GenerateConfig(configDictionary, configPath):
    directory = configPath.rpartition("/")[0]
    print(CheckDirExistsAndCreateIfNot(directory))

    #Create and add data to config file.
    with open(configPath, "w+") as f:
        json.dump(configDictionary, f)

    return ReadConfig(configPath)

def ReadConfig(configPath):
    #Opens the config file and reads the json data, storeing it in the configData dictionary. 
    with open(configPath, "r") as f:
        configData = json.load(f)
    
    return configData