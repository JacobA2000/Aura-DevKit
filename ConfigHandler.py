import json
import os
from pathlib import Path

def CheckDirExistsAndCreateIfNot(path):
    #Checks if a directory exists and if not creates it.
    if os.path.exists(path):
        return True
    else:
        os.mkdir(path)
        return f"Created directory {path}."

def GenerateConfig(configDictionary, configPath):
    directory = configPath.rpartition("/")[0]
    print(CheckDirExistsAndCreateIfNot(directory))

    #Create and add data to config file.
    with open(configPath, "w+") as f:
        json.dump(configDictionary, f)

def ReadConfig(configPath):
    #Opens the config file and reads the json data, storeing it in the configData dictionary. 
    with open(configPath, "r") as f:
        configData = json.load(f)
    
    return configData