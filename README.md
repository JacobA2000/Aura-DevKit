# Aura-DevKit 
<img src="https://raw.githubusercontent.com/JacobA2000/Aura-DevKit/main/img/Aura-DevKit-Logo-Small.png" alt="Aura-DevKit Logo" style="width:100px;"/>

## Contents
1. [Introduction](#introduction)
1. [Requirements](#requirements)
1. [CreateProject](#createproject) 
    * [About](#about-createproject)
    * [Installation](#createproject-installation)
1. [Adding Path Variable](#adding-path-variable)
    * [Windows](#windows)
    * [Linux](#linux)

***
## **Introduction**
Aura-DevKit is a collection of command line tools created to make the process of development easier. It does this by automating or shortening the time spent on dull tasks.

Aura-DevKit is made up of different modules and more will be added as development continues. The current modules are:

* [CreateProject](#createproject)

Aura-DevKit is cross-platform and should work on both Windows and Linux although the setup process varies between operating systems and the tool is currently built under windows so there may be more issues on linux, however I try to test it as much as possible.
***

## **Requirements**
In order for Aura-DevKit to function as intended we first have to meet a few requirements, these are as follows:

1. **At least Python3 or above (This is currently being developed in 3.8):**
    
    https://www.python.org/downloads/

1.  **External python packages used by Aura-DevKit ([list of packages used](https://raw.githubusercontent.com/JacobA2000/Aura-DevKit/main/requirements.txt))**

    Make sure to run this from inside the Aura-DevKit directory (or specify the full path of the requirements file.)

    ```sh
    pip install -r requirements.txt
    ```
***

## **CreateProject**
### **About CreateProject**
The CreateProject tool reduces the total number of commands needed to create a git repository for your project. It reduces the old process which required six commands to only one command.

* **Without** Aura-DevKit
    ```sh
    mkdir project
    cd project
    git init
    git add README.md
    git remote add origin git@github.com:username/new_repo
    git push -u origin main
    ```
* **With** Aura-DevKit
    ```sh
    createproject <name> <private>
    ```

    The \<name> and \<private> are optional parameters, if called without them createproject will default to asking the user to input a name, and will use the default value of true for private.

## **CreateProject Installation**
CreateProject can be run by just running the python file as you would any other, **however this is not the recommended way of doing so**. To run create project as intended there is a small amount of configuration required. This is as follows.

1. **In order for CreateProject to function the user needs to have git installed and an ssh key setup for their machine.**

    I will not be going into detail on how to do this in this readme but you can follow the steps [here](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/connecting-to-github-with-ssh) if you have not set one up yet.
1. **For the first launch we do have to run the file in the same way as we would any other python file:**
    ```python
    python CreateProject.py
    ```
    This will ensure that all of the correct directories and files are created.
    
    **During this process you will be required to input some information.**

    * **It will ask you where you wish your projects directory to be.**
    
        You should input the filepath of the directory you wish to store your projects in. **Ensure you end the path with the correct slash for your operating system e.g. windows: \\, linux: /**. An example of a valid and invalid file path is shown below:

        **Invalid filepath**
        ```
        ❌ E:\JACOB\Personal Projects\Active Projects\Aura-DevKit
        ```
        **Valid filepath**
        ```
        ✔️ E:\JACOB\Personal Projects\Active Projects\Aura-DevKit\
        ```

    * **You will also be asked to authenticate with GitHub via OAuth2** (This allows the program to create repositories on your behalf.)

        **You will be provided with a code in the terminal** (this lasts 15mins after this time has passed a new code will be generated). An example of what to look for is shown below:

        <img src="https://raw.githubusercontent.com/JacobA2000/Aura-DevKit/main/img/git-auth-code-example.png" alt="Auth Code Example"/>

        Approximately 5 seconds after receiving this message your default web browser should open to the webpage shown below:

        <img src="https://raw.githubusercontent.com/JacobA2000/Aura-DevKit/main/img/git-auth-webpage-example.png" alt="Auth Webpage Example" style="width:600px;"/>

        **You should enter the code from the terminal into the boxes on this webpage.**

        After doing so you should see this message in the terminal:
        <img src="https://raw.githubusercontent.com/JacobA2000/Aura-DevKit/main/img/git-auth-success-example.png" alt="Auth Code Example"/>

        This means that you have successfully authenticated with GitHub. From here you can either carry on and create a project by entering a name or kill the program.
1. **(Optional but strongly recommended) Add the shell folder to your PATH variable.**

    Although not essential, doing this is strongly recommended as it allows you to call the command from any location and also avoids the need to call python directly.

    For instructions on how to set this up click [here](#adding-path-variable).

(There are plans to reduce the complexity of setup in later updates)

***

## **Adding PATH Variable**

### **THIS ONLY NEEDS TO BE DONE ONCE NOT FOR EACH TOOL!**

#### **Windows**:
On windows we need to add our shell folder to our PATH environment variable. To do this we need to do the following:
1. Open the search bar and search for "edit environment variables for you account" and open it.
1. Click on the path variable in the user variables and hit edit.
1. Copy the path to the folder you saved the script in.
1. Hit new and paste the path you copied.
1. Press OK on both windows.

Now we should be able to open up a terminal(powershell, cmd, windows terminal, etc) and type createproject and it will execute the python script.

#### **Linux**:
On Linux we need to add our shell folder to our PATH environment variable. To do this we need to do the following:
1. cd into the shell folder
    ```bash
    cd shell
    ```
1. Give the shell script executable permissions.
    ```bash
    sudo chmod +x <scriptname>
    ```
    Replace \<scriptname> with the script you wish to make executeable e.g. for create project it would be createproject.sh.

1. cd to your home directory
    ```bash
    cd $HOME
    ```
1. Open up your terminals rc file (this file name varies depending on your terminal but in most distros, the default will be .bashrc, I have included some popular terminals rc files below) with your favorite text editor(I would recommend using vim)
    ```
    bash: ~/.bashrc

    zsh: ~/.zshrc
    ```
1. Add the following line, **MAKE SURE TO CHANGE /path/to/project/folder TO THE PATH OF YOUR SHELL FOLDER INSIDE OF THE MAIN PROJECT FOLDER**  
    ```bash
    export PATH=/path/to/project/folder:$PATH
    ```
1. Open a new terminal or reboot your machine

Now we should be able to open up the terminal and run our shell script by typing createproject.sh

