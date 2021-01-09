import sys
import urllib.parse
import webbrowser
from GeneralHandlers import ShellHandler

codePath = ""
codeString = ""
carbonURL = "https://carbon.now.sh/?"

ShellHandler.GenerateShellScript(__file__, 1)

if "help" in (x.lower() for x in sys.argv):
    print("""
    CodeToImage Help
    
    CodeToImage can be run in a few different ways. These are as follows:
    1.  codetoimage
    2.  codetoimage {filepath}

    The curly brackets({}) indicate arguments that can be passed, the arguments for this are as follows: 
    {filepath} - The filepath for the code you wish to convert to an image via carbon.

    If 1 is ran the user will be prompted to enter the details in the terminal.
    
    If 2 is ran carbon will open in the default browser with the code from the file displayed.
    """)
else:
    if len(sys.argv) == 2:
        codePath = sys.argv[1]

    if codePath == "":
        codePath = input("Please enter the path to the code file you wish to convert to an image. : ")

    with open(codePath, "r") as f:
        codeString = f.read()

    carbonURLParams = {
        "bg": "rgba(171, 184, 195, 1)", #Background
        "t": "seti", #Theme
        "wt": "none", #Window Controls Theme
        "l": "auto", #Language
        "ds": "true", #Drop Shadow
        "dsyoff": "20px", #Drop Shadow Y Offset
        "dsblur": "68px", #Drop Shadow Blur
        "wc": "true", #Window Controls
        "wa": "true", #Auto Adjust Width
        "pv": "56px", #Padding Vertical
        "ph": "56px", #Padding Horizontal
        "ln": "false", #Line Numbers
        "fl": "1", 
        "fm": "Hack", #Font
        "fs": "14px", #Font Size
        "lh": "133%25", #Line Height
        "si": "false", #Squared Image
        "es": "2x", #Export Size
        "wm": "false", #Watermark
        "code": codeString #The Code
        }

    carbonURL += urllib.parse.quote(urllib.parse.urlencode(carbonURLParams), safe="=&%+") 

    webbrowser.open(carbonURL)