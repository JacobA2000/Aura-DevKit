import json
import os

def check_dir_exists_create_if_not(path):
    #Checks if a directory exists and if not creates it.
    if os.path.exists(path):
        return True
    else:
        os.mkdir(path)
        print(f"[ConfigHandler] Created directory {path}.")
        return True

def check_if_config_exists(path):
    #Checks if a directory exists.
    if os.path.exists(path):
        return True
    else:
        return False

def check_get_config(config_path, config_template, user_input):
    #Checks if a config exists using the ConfigHandler and if so reads and stores the data in configData and returns it, if not it creates one in the correct format.
    if check_if_config_exists(config_path):
        config_data = read_config(config_path)
    else:
        config_data = generate_config(config_template, config_path, user_input)

    return config_data

def generate_config(config_dict, config_path, user_input):
    directory = config_path.rpartition("/")[0]
    check_dir_exists_create_if_not(directory)

    if user_input == True:
        #Loop through keys in config file and set values of keys based on user input.
        print(f"[ConfigHandler] A config file {config_path} that should exist doesn't, creating it now, please be prepared to provide information.")
        for key in config_dict:
            config_dict[key] = input(f"[ConfigHandler] Please enter the following information {key.upper()}: ")
    else:
        print(f"[ConfigHandler] A config file {config_path} that should exist doesn't, creating it now.")

    #Create and add data to config file.
    with open(config_path, "w+") as f:
        json.dump(config_dict, f)

    print(f"[ConfigHandler] Successfully generated config file: {config_path}.")

    return read_config(config_path)

def read_config(config_path):
    print(f"[ConfigHandler] Reading config file {config_path}.")
    #Opens the config file and reads the json data, storing it in the configData dictionary. 
    with open(config_path, "r") as f:
        config_data = json.load(f)
    
    return config_data

def update_config(config_path, config_data):
    print(f"[ConfigHandler] Updating config file {config_path}.")
    with open(config_path, "w+") as f:
        f.truncate(0)
        json.dump(config_data, f)