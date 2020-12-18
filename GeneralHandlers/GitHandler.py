import requests
import json
import subprocess
from GeneralHandlers import ConfigHandler

#Config infomation.
gitConfigData = {}

#Get the git information from the config file.
gitUsername = ""
gitToken = ""

def CheckAndSetGitConfig():
    #Checks if a git-config exists using the ConfigHandler and if so sets the username and token, if not it creates one in the correct format.
    global gitConfigData, gitUsername, gitToken

    gitConfigPath = "./cfg/git-config.json"
    gitConfigTemplate = {"gitUsername": "", "gitToken": ""}

    gitConfigData = ConfigHandler.CheckAndGetConfig(gitConfigPath, gitConfigTemplate)

    gitUsername = gitConfigData["gitUsername"]
    gitToken = gitConfigData["gitToken"]

def CreateRepo(name, private):
    #Creates a new GitHub repo via the GitHub api using the users login token.
    url = "https://api.github.com/user/repos"
    payload = {"name": name, "private": private, "auto_init": True}

    print(f"Creating Repository {name} for user {gitUsername}. Private: {private}.")
    r = requests.post(url, auth=(gitUsername, gitToken), data=json.dumps(payload))
    
    rJson = json.loads(r.text)

    if r.ok:
        print(f"Repository {name} created.")
    else:
        print(f"Error: {rJson['message']}")

    return rJson

def CloneRepo(sshURL, projectsDir):
    p = subprocess.Popen(['git', 'clone', str(sshURL), projectsDir])
    p.wait()
    p.terminate()