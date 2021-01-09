import os
import sys
from GeneralHandlers import FileHandler, ConfigHandler

def GenerateShellScript(fileToExecute, numArgs):
    mainDirPath = FileHandler.mainDirPath
    #Use ConfigHandler method to check if the shell directory exists.
    ConfigHandler.CheckDirExistsAndCreateIfNot(f"{mainDirPath}/shell")
    pythonName = os.path.basename(sys.executable)
    
    shellScriptName = os.path.splitext(os.path.basename((fileToExecute.lower())))[0]

    if os.name == "nt":
        #Checks if .bat file exists
        if os.path.exists(f"{mainDirPath}/shell/{shellScriptName}.bat") == False:
            #Create bat file to run quickly on windows.
            print(f"[CreateProject] Creating shell script at {mainDirPath}/shell/{shellScriptName}.bat...")
            with open(f"{mainDirPath}/shell/{shellScriptName}.bat", "w") as batf:
                batf.write(f"{pythonName} \"{fileToExecute}\"")
                
                for i in range(numArgs):
                    batf.write(f" %{i+1}")

            print(f"[CreateProject] Shell script successfully generated.")

    else:
        if os.path.exists(f"{mainDirPath}/shell/{shellScriptName}.sh") == False:
            #Create shell file to run quickly on linux.
            print(f"[CreateProject] Creating shell script at {mainDirPath}/shell/{shellScriptName}.sh...")
            with open(f"{mainDirPath}/shell/{shellScriptName}.sh", "w") as shf:
                shf.write(f"{pythonName} \"{mainDirPath}\{fileToExecute}\"")

                for i in range(numArgs):
                    shf.write(f" ${i+1}")

            print(f"[CreateProject] Shell script successfully generated.")