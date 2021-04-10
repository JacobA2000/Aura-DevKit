import os
import sys
from GeneralHandlers import FileHandler, ConfigHandler

def generate_shell_script(file_to_execute, arg_count):
    main_dir_path = FileHandler.main_dir_path
    #Use ConfigHandler method to check if the shell directory exists.
    ConfigHandler.check_dir_exists_create_if_not(f"{main_dir_path}/shell")
    python_name = os.path.basename(sys.executable)
    
    shell_script_name = os.path.splitext(os.path.basename((file_to_execute.lower())))[0]

    if os.name == "nt":
        #Checks if .bat file exists
        if os.path.exists(f"{main_dir_path}/shell/{shell_script_name}.bat") == False:
            #Create bat file to run quickly on windows.
            print(f"[CreateProject] Creating shell script at {main_dir_path}/shell/{shell_script_name}.bat...")
            with open(f"{main_dir_path}/shell/{shell_script_name}.bat", "w") as batf:
                batf.write(f"{python_name} \"{file_to_execute}\"")
                
                for i in range(arg_count):
                    batf.write(f" %{i+1}")

            print(f"[CreateProject] Shell script successfully generated.")

    else:
        if os.path.exists(f"{mainDirPath}/shell/{shellScriptName}.sh") == False:
            #Create shell file to run quickly on linux.
            print(f"[CreateProject] Creating shell script at {mainDirPath}/shell/{shellScriptName}.sh...")
            with open(f"{mainDirPath}/shell/{shellScriptName}.sh", "w") as shf:
                shf.write(f"{pythonName} \"{fileToExecute}\"")

                for i in range(numArgs):
                    shf.write(f" ${i+1}")

            print(f"[CreateProject] Shell script successfully generated.")