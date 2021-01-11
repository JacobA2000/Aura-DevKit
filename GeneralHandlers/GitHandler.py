import requests
import json
import subprocess
import webbrowser
import urllib 
import time
from GeneralHandlers import ConfigHandler, FileHandler

#Config infomation.
gitConfigData = {}

#Get the git information from the config file.
gitUsername = ""
gitToken = ""

def AuthorizeWithGit():
    #https://docs.github.com/en/free-pro-team@latest/developers/apps/authorizing-oauth-apps#device-flow
    deviceEndpointURL = 'https://github.com/login/device/code'

    deviceReq = requests.post(
        deviceEndpointURL, 
        data={
            "client_id": "62cff3fa8c2b640a4d02",
            "scope": "repo user"
        }
    )

    #Convert the returned url query string to a JSON style dictionary.
    deviceReqJson = dict(urllib.parse.parse_qsl(deviceReq.text))

    print(f"""
    [GitHandler] Git authentication required, a new browser tab will open soon asking for the code shown below.
                 CODE: {deviceReqJson['user_code']}""")
    time.sleep(5)
    webbrowser.open_new_tab("https://github.com/login/device")

    #Check every deviceReqJson[interval] seconds for response.
    while True:
        tokenEndpointURL = 'https://github.com/login/oauth/access_token'

        tokenReq = requests.post(
            tokenEndpointURL, 
            data={
                "client_id": "62cff3fa8c2b640a4d02",
                "device_code": deviceReqJson["device_code"],
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code"
            }
        )

        tokenReqJson = dict(urllib.parse.parse_qsl(tokenReq.text))

        if "access_token" in tokenReqJson:
            gitConfigData = ConfigHandler.ReadConfig(f"{FileHandler.mainDirPath}/cfg/git-config.json")
            gitConfigData["gitToken"] = tokenReqJson["access_token"]
            ConfigHandler.SaveConfig(f"{FileHandler.mainDirPath}/cfg/git-config.json", gitConfigData)
            break

        time.sleep(int(deviceReqJson["interval"]))


def CheckAndSetGitConfig():
    #Checks if a git-config exists using the ConfigHandler and if so sets the username and token, if not it creates one in the correct format.
    global gitConfigData, gitUsername, gitToken

    mainDirPath = FileHandler.mainDirPath

    gitConfigPath = f"{mainDirPath}/cfg/git-config.json"
    gitConfigTemplate = {"gitUsername": "", "gitToken": ""}

    gitConfigData = ConfigHandler.CheckAndGetConfig(gitConfigPath, gitConfigTemplate)

    gitUsername = gitConfigData["gitUsername"]
    gitToken = gitConfigData["gitToken"]

def CreateRepo(name, private):
    #Creates a new GitHub repo via the GitHub api using the users login token.
    url = "https://api.github.com/user/repos"
    payload = {"name": name, "private": private, "auto_init": True}

    print(f"[GitHandler] Creating Repository {name} for user {gitUsername}. Private: {private}.")
    r = requests.post(url, auth=(gitUsername, gitToken), data=json.dumps(payload))
    
    rJson = json.loads(r.text)

    if r.ok:
        print(f"[GitHandler] Repository {name} created.")
    else:
        print(f"[GitHandler] Error: {rJson['message']}")

    return rJson

def CloneRepo(sshURL, projectsDir):
    #Starts a clone using the ssh clone url (User will of needed to setup an ssh key with github for this to work), Starts a clone subprocess, waits for it to finish then temrinates it.
    print(f"[GitHandler] Starting Clone from {sshURL}")
    p = subprocess.Popen(['git', 'clone', str(sshURL), projectsDir])
    p.wait()
    p.terminate()
    print(f"[GitHandler] Clone Complete.")
