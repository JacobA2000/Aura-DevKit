import sys
import os
from GeneralHandlers import ConfigHandler, ProjectsHandler, GitHandler
from SupportScripts import ConsoleColours

def GenerateShellScript():
    #Use ConfigHandler method to check if the shell directory exists.
    ConfigHandler.CheckDirExistsAndCreateIfNot("./shell")
    pythonName = os.path.basename(sys.executable)
    
    if os.name == "nt":
        #Checks if .bat file exists
        if os.path.exists("./shell/createproject.bat") == False:
            #Create bat file to run quickly on windows.
            print(f"{ConsoleColours.bcolours.BOLD}[CreateProject]{ConsoleColours.bcolours.ENDC} {ConsoleColours.bcolours.OKCYAN}Creating shell script at {os.getcwd()}/shell/createproject.bat ...{ConsoleColours.bcolours.ENDC}")
            with open("./shell/createproject.bat", "w") as batf:
                batf.write(f"{pythonName} \"{__file__}\" %1 %2")
            print(f"{ConsoleColours.bcolours.BOLD}[CreateProject]{ConsoleColours.bcolours.ENDC} {ConsoleColours.bcolours.OKGREEN}Shell script successfully generated.{ConsoleColours.bcolours.ENDC}")

    else:
        if os.path.exists("./shell/createproject.sh") == False:
            #Create shell file to run quickly on linux.
            print(f"{ConsoleColours.bcolours.BOLD}[CreateProject]{ConsoleColours.bcolours.ENDC} {ConsoleColours.bcolours.OKCYAN}Creating shell script at {os.getcwd()}/shell/createproject.sh ...{ConsoleColours.bcolours.ENDC}")
            with open("./shell/createproject.sh", "w") as batf:
                batf.write(f"{pythonName} \"{os.getcwd() + __file__}\" %1 %2")
            print(f"{ConsoleColours.bcolours.BOLD}[CreateProject]{ConsoleColours.bcolours.ENDC} {ConsoleColours.bcolours.OKGREEN}Shell script successfully generated.{ConsoleColours.bcolours.ENDC}")

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
        print(f"{ConsoleColours.bcolours.BOLD}[CreateProject]{ConsoleColours.bcolours.ENDC} {ConsoleColours.bcolours.WARNING}Incorrect value for private argument, please only enter true or false.\nContinuing using the default value of True. This can be changed on the GitHub website if incorrect.{ConsoleColours.bcolours.ENDC}")
        private = True

#Check configs are correct.
ProjectsHandler.CheckAndSetProjectsConfig()
GitHandler.CheckAndSetGitConfig()

#Create the project.
ProjectsHandler.CreateProject(name, private)


