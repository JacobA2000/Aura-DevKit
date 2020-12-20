import os

mainDirPath = ""

if os.name == "nt":
    mainDirPath = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
else:
    mainDirPath = os.path.dirname(os.path.abspath(__file__))