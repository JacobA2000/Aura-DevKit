import os
from GeneralHandlers import ConfigHandler, GitHandler, FileHandler

projectsConfigData = {}
projectsDir = ""

def CheckAndSetProjectsConfig():
    #Checks if a git-config exists using the ConfigHandler and if so sets the username and token, if not it creates one in the correct format.
    global projectsDir, projectsConfigData

    mainDirPath = FileHandler.mainDirPath

    projectsConfigPath = f"{mainDirPath}/cfg/projects-config.json"
    projectsConfigTemplate = {"projectsDir": ""}

    projectsConfigData = ConfigHandler.CheckAndGetConfig(projectsConfigPath, projectsConfigTemplate)

    projectsDir = projectsConfigData["projectsDir"]

def OpenProjectDirectory(path):
    print(f"[ProjectsHandler] Opening Project Directory...")
    if os.name == "nt":
        os.startfile(path)
    else:
        os.system(f"xdg-open {path}")
    print(f"[ProjectsHandler] Opened Project Directory.")

def CreateProject(name="", private=True):
    #Creates a git repo and clones it into the projects directory.
    global projectsDir

    if name == "":
        name = input(f"[ProjectsHandler] Project Name: ")

    gitRepo = GitHandler.CreateRepo(name, private)
    sshURL = gitRepo["ssh_url"]

    cloneLocation = projectsDir + name

    GitHandler.CloneRepo(sshURL, cloneLocation)
    OpenProjectDirectory(cloneLocation)