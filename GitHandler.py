import requests
import json
import ConfigHandler

#Get the config infomation
configData = ConfigHandler.ReadConfig("./cfg/git-config.json")

#Get the git information from the config file.
gitUsername = configData["gitUserName"]
gitToken = configData["gitToken"]

#Creates a new GitHub repo via the GitHub api using the users login token.
def CreateRepo(name, visibility):
    url = "https://api.github.com/user/repos"
    payload = {"name": name, "private": visibility, "auto_init": True}

    r = requests.post(url, auth=(gitUsername, gitToken), data=json.dumps(payload))
    rJson = json.loads(r.text)

    return rJson
