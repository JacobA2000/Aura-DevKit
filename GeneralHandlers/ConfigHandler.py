import json
import os
from SupportScripts import ConsoleColours 

def CheckDirExistsAndCreateIfNot(path):
    #Checks if a directory exists and if not creates it.
    if os.path.exists(path):
        return True
    else:
        os.mkdir(path)
        print(f"{ConsoleColours.bcolours.BOLD}[ConfigHandler]{ConsoleColours.bcolours.ENDC} {ConsoleColours.bcolours.OKGREEN}Created directory {path}{ConsoleColours.bcolours.ENDC}.")
        return True

def CheckIfConfigExists(path):
    #Checks if a directory exists.
    if os.path.exists(path):
        return True
    else:
        return False

def CheckAndGetConfig(configPath, configTemplate):
    #Checks if a config exists using the ConfigHandler and if so reads and stores the data in configData and returns it, if not it creates one in the correct format.
    if CheckIfConfigExists(configPath):
        gitConfigData = ReadConfig(configPath)
    else:
        gitConfigData = GenerateConfig(configTemplate, configPath)

    return gitConfigData

def GenerateConfig(configDictionary, configPath):
    directory = configPath.rpartition("/")[0]
    CheckDirExistsAndCreateIfNot(directory)

    #Loop through keys in config file and set values of keys based on user input.
    print(f"{ConsoleColours.bcolours.BOLD}[ConfigHandler]{ConsoleColours.bcolours.ENDC} {ConsoleColours.bcolours.OKCYAN}A config file {configPath} that should exist doesn't, creating it now, please be prepared to provide information.{ConsoleColours.bcolours.ENDC}")
    for key in configDictionary:
        configDictionary[key] = input(f"{ConsoleColours.bcolours.BOLD}[ConfigHandler]{ConsoleColours.bcolours.ENDC} {ConsoleColours.bcolours.OKCYAN}Please enter the following information {key.upper()}: {ConsoleColours.bcolours.ENDC}")

    #Create and add data to config file.
    with open(configPath, "w+") as f:
        json.dump(configDictionary, f)

    print(f"{ConsoleColours.bcolours.BOLD}[ConfigHandler]{ConsoleColours.bcolours.ENDC} {ConsoleColours.bcolours.OKGREEN}Successfully generated config file: {configPath}.{ConsoleColours.bcolours.ENDC}")

    return ReadConfig(configPath)

def ReadConfig(configPath):
    #Opens the config file and reads the json data, storeing it in the configData dictionary. 
    with open(configPath, "r") as f:
        configData = json.load(f)
    
    return configData