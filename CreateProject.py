import sys
import os
from GeneralHandlers import ConfigHandler, ProjectsHandler, GitHandler, FileHandler, ShellHandler

name = ""
private = None

ShellHandler.generate_shell_script(__file__, 2)

if "help" in (x.lower() for x in sys.argv):
    print("""
    CreateProject Help
    
    CreateProject can be run in a few different ways. These are as follows:
    1.  createproject
    2.  createproject {name}
    3.  createproject {name}{private}

    The curly brackets({}) indicate arguments that can be passed, the arguments for this are as follows: 
    {name} - The name you wish to give to the repository.
    {private} - The visibility of the project, this can either be true or false. 
                    True will create a private repository, 
                    False will create a public repository. 

    If 1 is ran the user will be prompted to enter the details in the terminal.
    
    If 2 is ran the repository will be created with the specified name, this repository will be private.

    If 3 is ran the repository will be created with the specified name and visibility.
    """)
else:
    if len(sys.argv) == 2:
        name = str(sys.argv[1])
        #If no argument for private given presume private = true for security reasons
        private = True
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
    ProjectsHandler.check_set_projects_config(user_input=True)
    GitHandler.check_and_set_git_config(user_input=False)

    #Create the project.
    ProjectsHandler.create_project(name, private)