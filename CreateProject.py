import sys
from GeneralHandlers import ConfigHandler, ProjectsHandler, GitHandler

name = ""
private = True

print(len(sys.argv))
if len(sys.argv) == 2:
    name = str(sys.argv[1])
if len(sys.argv) == 3:
    name = str(sys.argv[1])
    private = str(sys.argv[2])

    #Convert private str into bool.
    if private.lower() == "false":
        private = False
    elif private.lower() == "true":
        private = True

#Check configs are correct.
ProjectsHandler.CheckAndSetProjectsConfig()
GitHandler.CheckAndSetGitConfig()

#Create the project.
ProjectsHandler.CreateProject()