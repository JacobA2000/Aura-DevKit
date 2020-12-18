import requests
import json
import subprocess
from GeneralHandlers import ConfigHandler
from SupportScripts import ConsoleColours

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

    print(f"{ConsoleColours.bcolours.BOLD}[GitHandler]{ConsoleColours.bcolours.ENDC} {ConsoleColours.bcolours.OKCYAN}Creating Repository {name} for user {gitUsername}. Private: {private}.{ConsoleColours.bcolours.ENDC}")
    r = requests.post(url, auth=(gitUsername, gitToken), data=json.dumps(payload))
    
    rJson = json.loads(r.text)

    if r.ok:
        print(f"{ConsoleColours.bcolours.BOLD}[GitHandler]{ConsoleColours.bcolours.ENDC} {ConsoleColours.bcolours.OKGREEN}Repository {name} created.{ConsoleColours.bcolours.ENDC}")
    else:
        print(f"{ConsoleColours.bcolours.BOLD}[GitHandler]{ConsoleColours.bcolours.ENDC} {ConsoleColours.bcolours.FAIL}Error: {rJson['message']}{ConsoleColours.bcolours.ENDC}")

    return rJson

def CloneRepo(sshURL, projectsDir):
    #Starts a clone using the ssh clone url (User will of needed to setup an ssh key with github for this to work), Starts a clone subprocess, waits for it to finish then temrinates it.
    print(f"{ConsoleColours.bcolours.BOLD}[GitHandler]{ConsoleColours.bcolours.ENDC} {ConsoleColours.bcolours.OKCYAN}Starting Clone from {sshURL}{ConsoleColours.bcolours.ENDC}")
    p = subprocess.Popen(['git', 'clone', str(sshURL), projectsDir])
    p.wait()
    p.terminate()
    print(f"{ConsoleColours.bcolours.BOLD}[GitHandler]{ConsoleColours.bcolours.ENDC} {ConsoleColours.bcolours.OKGREEN}Clone Complete{ConsoleColours.bcolours.ENDC}")
