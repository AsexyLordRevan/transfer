import os
import json
home= os.path.expanduser("~")
os.chdir(home+"/.config/asexy/configs")
commands=json.load(open("commands.json"))
for command in commands:
    os.system(command)