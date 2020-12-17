import requests
import json
from GeneralHandlers import ConfigHandler

#Config infomation.
gitConfigData = {}

#Get the git information from the config file.
gitUsername = ""
gitToken = ""

def CheckAndGetGitConfig():
    #Checks if a git-config exists using the ConfigHandler and if so sets the username and token, if not it creates one in the correct format.
    global gitConfigData, gitUsername, gitToken

    gitConfigPath = "./cfg/git-config.json"
    gitConfigTemplate = {"gitUsername": "", "gitToken": ""}

    if ConfigHandler.CheckIfConfigExists(gitConfigPath):
        gitConfigData = ConfigHandler.ReadConfig(gitConfigPath)
    else:
        gitConfigData = ConfigHandler.GenerateConfig(gitConfigTemplate, gitConfigPath)

    gitUsername = gitConfigData["gitUsername"]
    gitToken = gitConfigData["gitToken"]

def CreateRepo(name, visibility):
    #Creates a new GitHub repo via the GitHub api using the users login token.
    url = "https://api.github.com/user/repos"
    payload = {"name": name, "private": visibility, "auto_init": True}

    print(f"Creating Repository {name} for user {gitUsername}. Private: {visibility}.")
    r = requests.post(url, auth=(gitUsername, gitToken), data=json.dumps(payload))
    
    if r.ok:
        print(f"Repository {name} created.")
    else:
        print(r.text)

    rJson = json.loads(r.text)
    return rJson