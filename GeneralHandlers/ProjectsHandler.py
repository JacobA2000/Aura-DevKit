from GeneralHandlers import ConfigHandler, GitHandler

projectsConfigData = {}
projectsDir = ""

def CheckAndSetProjectsConfig():
    #Checks if a git-config exists using the ConfigHandler and if so sets the username and token, if not it creates one in the correct format.
    global projectsDir, projectsConfigData

    projectsConfigPath = "./cfg/projects-config.json"
    projectsConfigTemplate = {"projectsDir": ""}

    projectsConfigData = ConfigHandler.CheckAndGetConfig(projectsConfigPath, projectsConfigTemplate)

    projectsDir = projectsConfigData["projectsDir"]

def CreateProject(name="", private=True):
    #Creates a git repo and clones it into the projects directory.
    global projectsDir

    if name == "":
        name = input("Project Name: ")

    gitRepo = GitHandler.CreateRepo(name, private)
    sshURL = gitRepo["ssh_url"]

    cloneLocation = projectsDir + name

    GitHandler.CloneRepo(sshURL, cloneLocation)