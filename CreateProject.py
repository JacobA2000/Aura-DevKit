import sys
import os
from GeneralHandlers import ConfigHandler, ProjectsHandler, GitHandler

def GenerateShellScript():
    #Use ConfigHandler method to check if the shell directory exists.
    ConfigHandler.CheckDirExistsAndCreateIfNot("./shell")
    pythonName = os.path.basename(sys.executable)
    
    if os.name == "nt":
        #Checks if .bat file exists
        if os.path.exists("./shell/createproject.bat") == False:
            #Create bat file to run quickly on windows.
            with open("./shell/createproject.bat", "w") as batf:
                batf.write(f"{pythonName} \"{__file__}\" %1 %2")

    else:
        if os.path.exists("./shell/createproject.sh") == False:
            #Create shell file to run quickly on linux.
            with open("./shell/createproject.sh", "w") as batf:
                batf.write(f"{pythonName} \"{__file__}\" %1 %2")

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
        print("Incorrect value for private argument, please only enter true or false.\nContinuing using the default value of True. This can be changed on the GitHub website if incorrect.")
        private = True

#Check configs are correct.
ProjectsHandler.CheckAndSetProjectsConfig()
GitHandler.CheckAndSetGitConfig()

#Create the project.
ProjectsHandler.CreateProject(name, private)


