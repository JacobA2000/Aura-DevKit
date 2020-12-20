import sys
import os
from GeneralHandlers import ConfigHandler, ProjectsHandler, GitHandler, FileHandler

def GenerateShellScript():
    mainDirPath = FileHandler.mainDirPath
    #Use ConfigHandler method to check if the shell directory exists.
    ConfigHandler.CheckDirExistsAndCreateIfNot(f"{mainDirPath}/shell")
    pythonName = os.path.basename(sys.executable)
    
    if os.name == "nt":
        #Checks if .bat file exists
        if os.path.exists(f"{mainDirPath}/shell/createproject.bat") == False:
            #Create bat file to run quickly on windows.
            print(f"[CreateProject] Creating shell script at {mainDirPath}/shell/createproject.bat...")
            with open(f"{mainDirPath}/shell/createproject.bat", "w") as batf:
                batf.write(f"{pythonName} \"{__file__}\" %1 %2")
            print(f"[CreateProject] Shell script successfully generated.")

    else:
        if os.path.exists(f"{mainDirPath}/shell/createproject.sh") == False:
            #Create shell file to run quickly on linux.
            print(f"[CreateProject] Creating shell script at {mainDirPath}/shell/createproject.sh...")
            with open(f"{mainDirPath}/shell/createproject.sh", "w") as shf:
                shf.write(f"{pythonName} \"{mainDirPath}/{__file__}\" $1 $2")
            print(f"[CreateProject] Shell script successfully generated.")

name = ""
private = True

GenerateShellScript()

if len(sys.argv) == 2:
    name = str(sys.argv[1])
elif len(sys.argv) >= 3:
    name = str(sys.argv[1])
    private = str(sys.argv[2])

    #Convert private str into bool.
    if private.lower() == "false":
        private = False
    elif private.lower() == "true":
        private = True
    else:
        print(f"[CreateProject] Incorrect value for private argument, please only enter true or false.\nContinuing using the default value of True. This can be changed on the GitHub website if incorrect.")
        private = True

#Check configs are correct.
ProjectsHandler.CheckAndSetProjectsConfig()
GitHandler.CheckAndSetGitConfig()

#Create the project.
ProjectsHandler.CreateProject(name, private)


