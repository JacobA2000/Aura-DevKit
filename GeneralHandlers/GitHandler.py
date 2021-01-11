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
    clientID = "62cff3fa8c2b640a4d02"
    deviceEndpointURL = 'https://github.com/login/device/code'

    deviceReq = requests.post(
        deviceEndpointURL, 
        data={
            "client_id": clientID,
            "scope": "repo user"
        }
    )

    #Get the time we recieved a response.
    startTime = time.time()

    #Convert the returned url query string to a JSON style dictionary.
    deviceReqJson = dict(urllib.parse.parse_qsl(deviceReq.text))

    print(f"""
    [GitHandler] Git authentication required, a new browser tab will open soon asking for the code shown below.
                 CODE: {deviceReqJson['user_code']}""")
    time.sleep(5)
    webbrowser.open_new_tab(deviceReqJson["verification_uri"])

    #Send new post to check for access token every deviceReqJson[interval] seconds.
    while True:
        #Send the post request.
        tokenEndpointURL = 'https://github.com/login/oauth/access_token'

        tokenReq = requests.post(
            tokenEndpointURL, 
            data={
                "client_id": clientID,
                "device_code": deviceReqJson["device_code"],
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code"
            }
        )

        #Convert the returned url query string to a JSON style dictionary.
        tokenReqJson = dict(urllib.parse.parse_qsl(tokenReq.text))

        #Check for token
        if "access_token" in tokenReqJson:
            #Save token to config file.
            gitConfigData = ConfigHandler.ReadConfig(f"{FileHandler.mainDirPath}/cfg/git-config.json")
            gitConfigData["gitToken"] = tokenReqJson["access_token"]
            ConfigHandler.UpdateConfig(f"{FileHandler.mainDirPath}/cfg/git-config.json", gitConfigData)
            print(f"[GitHandler] User succesfully authenticated via device flow. Authentication can be revoked at any time via this url https://github.com/settings/connections/applications/{clientID}")
            break
        
        #Check if the code has timed out yet.
        currentTime = time.time()
        if (currentTime - int(deviceReqJson["expires_in"])) >= startTime:
            print("[GitHandler] CODE TIMED OUT! Generating new code in 5 seconds...")
            time.sleep(5)
            #Recursively call this function to start the auth process again.
            AuthorizeWithGit()
            #If the function has been recursively called we do not want to sleep for 5 seconds 
            #once authenticated so we break from the loop here.
            break

        #Wait for the interval.
        time.sleep(int(deviceReqJson["interval"]))


def CheckAndSetGitConfig(userInput):
    #Checks if a git-config exists using the ConfigHandler and if so sets the username and token, if not it creates one in the correct format.
    global gitConfigData, gitUsername, gitToken

    mainDirPath = FileHandler.mainDirPath

    gitConfigPath = f"{mainDirPath}/cfg/git-config.json"
    gitConfigTemplate = {"gitToken": ""}

    gitConfigData = ConfigHandler.CheckAndGetConfig(gitConfigPath, gitConfigTemplate, userInput)

    #If no token perform OAuth Device code method.
    if gitConfigData["gitToken"] == "":
        #Call the OAuth code. 
        AuthorizeWithGit()
        #Update gitConfigData with new data entered into file.
        gitConfigData = ConfigHandler.ReadConfig(gitConfigPath)

    gitToken = gitConfigData["gitToken"]

def CreateRepo(name, private):
    #Creates a new GitHub repo via the GitHub api using the users login token.
    url = "https://api.github.com/user/repos"
    headers = {"Authorization": f"token {gitToken}"}
    payload = {"name": name, "private": private, "auto_init": True}

    print(f"[GitHandler] Creating Repository {name} for user {gitUsername}. Private: {private}.")
    #OLD AUTH METHOD r = requests.post(url, auth=(gitUsername, gitToken), data=json.dumps(payload))
    r = requests.post(url, headers=headers, data=json.dumps(payload))
    
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
