import requests
import json
import subprocess
import webbrowser
import urllib 
import time
from GeneralHandlers import ConfigHandler, FileHandler

#Config infomation.
git_config_data = {}

#Get the git information from the config file.
git_username = ""
git_token = ""

def authorize_with_git():
    #https://docs.github.com/en/free-pro-team@latest/developers/apps/authorizing-oauth-apps#device-flow
    client_id = "62cff3fa8c2b640a4d02"
    devicecode_endpoint = 'https://github.com/login/device/code'

    device_request = requests.post(
        devicecode_endpoint, 
        data={
            "client_id": client_id,
            "scope": "repo user"
        }
    )

    #Get the time we recieved a response.
    start_time = time.time()

    #Convert the returned url query string to a JSON style dictionary.
    device_request_json = dict(urllib.parse.parse_qsl(device_request.text))

    print(f"""
    [GitHandler] Git authentication required, a new browser tab will open soon asking for the code shown below.
                 CODE: {device_request_json['user_code']}""")
    time.sleep(5)
    webbrowser.open_new_tab(device_request_json["verification_uri"])

    #Send new post to check for access token every deviceReqJson[interval] seconds.
    while True:
        #Send the post request.
        token_endpoint = 'https://github.com/login/oauth/access_token'

        token_request = requests.post(
            token_endpoint, 
            data={
                "client_id": client_id,
                "device_code": device_request_json["device_code"],
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code"
            }
        )

        #Convert the returned url query string to a JSON style dictionary.
        token_request_json = dict(urllib.parse.parse_qsl(token_request.text))

        #Check for token
        if "access_token" in token_request_json:
            #Save token to config file.
            git_config_data = ConfigHandler.read_config(f"{FileHandler.main_dir_path}/cfg/git-config.json")
            git_config_data["gitToken"] = token_request_json["access_token"]
            ConfigHandler.update_config(f"{FileHandler.main_dir_path}/cfg/git-config.json", git_config_data)
            print(f"[GitHandler] User succesfully authenticated via device flow. Authentication can be revoked at any time via this url https://github.com/settings/connections/applications/{client_id}")
            break
        
        #Check if the code has timed out yet.
        current_time = time.time()
        if (current_time - int(device_request_json["expires_in"])) >= start_time:
            print("[GitHandler] CODE TIMED OUT! Generating new code in 5 seconds...")
            time.sleep(5)
            #Recursively call this function to start the auth process again.
            authorize_with_git()
            #If the function has been recursively called we do not want to sleep for 5 seconds 
            #once authenticated so we break from the loop here.
            break

        #Wait for the interval.
        time.sleep(int(device_request_json["interval"]))


def check_and_set_git_config(user_input):
    #Checks if a git-config exists using the ConfigHandler and if so sets the username and token, if not it creates one in the correct format.
    global git_config_data, git_username, git_token

    main_dir_path = FileHandler.main_dir_path

    git_config_path = f"{main_dir_path}/cfg/git-config.json"
    git_config_template = {"gitToken": ""}

    git_config_data = ConfigHandler.check_get_config(git_config_path, git_config_template, user_input)

    #If no token perform OAuth Device code method.
    if git_config_data["gitToken"] == "":
        #Call the OAuth code. 
        authorize_with_git()
        #Update gitConfigData with new data entered into file.
        git_config_data = ConfigHandler.read_config(git_config_path)

    git_token = git_config_data["gitToken"]

def create_repository(name, private):
    #Creates a new GitHub repo via the GitHub api using the users login token.
    url = "https://api.github.com/user/repos"
    headers = {"Authorization": f"token {git_token}"}
    payload = {"name": name, "private": private, "auto_init": True}

    print(f"[GitHandler] Creating Repository {name} for user {git_username}. Private: {private}.")
    #OLD AUTH METHOD r = requests.post(url, auth=(gitUsername, gitToken), data=json.dumps(payload))
    r = requests.post(url, headers=headers, data=json.dumps(payload))
    
    returned_json = json.loads(r.text)

    if r.ok:
        print(f"[GitHandler] Repository {name} created.")
    else:
        print(f"[GitHandler] Error: {returned_json['message']}")

    return returned_json

def clone_repository(ssh_url, projects_dir):
    #Starts a clone using the ssh clone url (User will of needed to setup an ssh key with github for this to work), Starts a clone subprocess, waits for it to finish then temrinates it.
    print(f"[GitHandler] Starting Clone from {ssh_url}")
    p = subprocess.Popen(['git', 'clone', str(ssh_url), projects_dir])
    p.wait()
    p.terminate()
    print(f"[GitHandler] Clone Complete.")
