import json
import os

def CheckDirExistsAndCreateIfNot(path):
    #Checks if a directory exists and if not creates it.
    if os.path.exists(path):
        return True
    else:
        os.mkdir(path)
        print(f"[ConfigHandler] Created directory {path}.")
        return True

def CheckIfConfigExists(path):
    #Checks if a directory exists.
    if os.path.exists(path):
        return True
    else:
        return False

def CheckAndGetConfig(configPath, configTemplate, userInput):
    #Checks if a config exists using the ConfigHandler and if so reads and stores the data in configData and returns it, if not it creates one in the correct format.
    if CheckIfConfigExists(configPath):
        configData = ReadConfig(configPath)
    else:
        configData = GenerateConfig(configTemplate, configPath, userInput)

    return configData

def GenerateConfig(configDictionary, configPath, userInput):
    directory = configPath.rpartition("/")[0]
    CheckDirExistsAndCreateIfNot(directory)

    if userInput == True:
        #Loop through keys in config file and set values of keys based on user input.
        print(f"[ConfigHandler] A config file {configPath} that should exist doesn't, creating it now, please be prepared to provide information.")
        for key in configDictionary:
            configDictionary[key] = input(f"[ConfigHandler] Please enter the following information {key.upper()}: ")
    else:
        print(f"[ConfigHandler] A config file {configPath} that should exist doesn't, creating it now.")

    #Create and add data to config file.
    with open(configPath, "w+") as f:
        json.dump(configDictionary, f)

    print(f"[ConfigHandler] Successfully generated config file: {configPath}.")

    return ReadConfig(configPath)

def ReadConfig(configPath):
    print(f"[ConfigHandler] Reading config file {configPath}.")
    #Opens the config file and reads the json data, storing it in the configData dictionary. 
    with open(configPath, "r") as f:
        configData = json.load(f)
    
    return configData

def UpdateConfig(configPath, configData):
    print(f"[ConfigHandler] Updating config file {configPath}.")
    with open(configPath, "w+") as f:
        f.truncate(0)
        json.dump(configData, f)