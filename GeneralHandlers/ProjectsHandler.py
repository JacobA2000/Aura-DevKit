import os
from GeneralHandlers import ConfigHandler, GitHandler, FileHandler

projects_config_data = {}
projects_dir = ""

def check_set_projects_config(user_input):
    #Checks if a git-config exists using the ConfigHandler and if so sets the username and token, if not it creates one in the correct format.
    global projects_dir, projects_config_data

    mainDirPath = FileHandler.main_dir_path

    projectsConfigPath = f"{mainDirPath}/cfg/projects-config.json"
    projectsConfigTemplate = {"projectsDir": ""}

    projects_config_data = ConfigHandler.check_get_config(projectsConfigPath, projectsConfigTemplate, user_input)

    projects_dir = projects_config_data["projectsDir"]

def open_project_directory(path):
    print(f"[ProjectsHandler] Opening Project Directory...")
    if os.name == "nt":
        os.startfile(path)
    else:
        os.system(f"xdg-open {path}")
    print(f"[ProjectsHandler] Opened Project Directory.")

def create_project(name="", private=True):
    #Creates a git repo and clones it into the projects directory.
    global projects_dir

    if name == "":
        name = input(f"[ProjectsHandler] Project Name: ")
    
    if len(name) > 100:
        print(f"The character limit for a git repo name is 100 characters, your name was {len(name)} characters.")
    else:
        git_repository = GitHandler.create_repository(name, private)
        ssh_url = git_repository["ssh_url"]

        clone_path = projects_dir + name

        GitHandler.clone_repository(ssh_url, clone_path)
        open_project_directory(clone_path)