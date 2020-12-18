import os
from GeneralHandlers import ConfigHandler, GitHandler
from SupportScripts import ConsoleColours

projectsConfigData = {}
projectsDir = ""

def CheckAndSetProjectsConfig():
    #Checks if a git-config exists using the ConfigHandler and if so sets the username and token, if not it creates one in the correct format.
    global projectsDir, projectsConfigData

    projectsConfigPath = "./cfg/projects-config.json"
    projectsConfigTemplate = {"projectsDir": ""}

    projectsConfigData = ConfigHandler.CheckAndGetConfig(projectsConfigPath, projectsConfigTemplate)

    projectsDir = projectsConfigData["projectsDir"]

def OpenProjectDirectory(path):
    print(f"{ConsoleColours.bcolours.BOLD}[ProjectsHandler]{ConsoleColours.bcolours.ENDC} {ConsoleColours.bcolours.OKCYAN}Opening Project Directory...{ConsoleColours.bcolours.ENDC}")
    if os.name == "nt":
        os.startfile(path)
    else:
        os.system(f"xdg-open {path}")
    print(f"{ConsoleColours.bcolours.BOLD}[ProjectsHandler]{ConsoleColours.bcolours.ENDC} {ConsoleColours.bcolours.OKGREEN}Opened Project Directory.{ConsoleColours.bcolours.ENDC}")

def CreateProject(name="", private=True):
    #Creates a git repo and clones it into the projects directory.
    global projectsDir

    if name == "":
        name = input(f"{ConsoleColours.bcolours.BOLD}[ProjectsHandler]{ConsoleColours.bcolours.ENDC} {ConsoleColours.bcolours.OKCYAN}Project Name: {ConsoleColours.bcolours.ENDC}")

    gitRepo = GitHandler.CreateRepo(name, private)
    sshURL = gitRepo["ssh_url"]

    cloneLocation = projectsDir + name

    GitHandler.CloneRepo(sshURL, cloneLocation)
    OpenProjectDirectory(cloneLocation)