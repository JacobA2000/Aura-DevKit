import sys
from GeneralHandlers import ConfigHandler, ProjectsHandler, GitHandler

name = ""
private = True

print(len(sys.argv))
if len(sys.argv) == 2:
    name = str(sys.argv[1])
if len(sys.argv) >= 3:
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