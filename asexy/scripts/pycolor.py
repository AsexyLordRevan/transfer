#Importing necessary modules
import os
import subprocess
import argparse
from json import load

#For importing config files
def json_load(file):
    with open(file) as f:
        return load(f)

#Create directories if they don't exist, moving to the colours directory
home=os.environ['HOME']
os.path.join(home, ".config/colours")
if not os.path.exists(home+"/.config/colours"):
    os.makedirs(os.path.join(home, ".config/colours"))
if not os.path.exists(home+"/.config/colours/colorschemes"):
    os.makedirs(os.path.join(home, ".config/colours/colorschemes"))
if not os.path.exists(home+"/.config/colours/generated"):
    os.makedirs(os.path.join(home, ".config/colours/generated"))
os.chdir(os.path.join(home, ".config/colours"))

#Get Colours
colorscheme = str(subprocess.check_output("rofi -show filebrowser -config ~/.config/rofi/icons.rasi -filebrowser-command 'echo' -modes filebrowser -filebrowser-directory "+home+"/.config/rofi/icons", shell=True))
colorscheme = colorscheme.replace(home+"/.config/rofi/icons/", "")
colorscheme = str(colorscheme.replace(".png",".json"))[2:-3]
if colorscheme == "":
    print("No theme selected, exiting")
    exit()

#Get necessary config file locations, get colourscheme
softList = json_load(os.path.join(home,".config/asexy/configs/software.json"))
colList = json_load(os.path.join(home,".config/colours/colorschemes/"+colorscheme))

#Function to set colours
def setcolors(colorscheme):
    new_colors = list(colList.values())
    new_names = list(colList.keys())
    # Create colour files
    with open(os.path.join(home,".config/colours/generated/coloursgtk.css"), "w") as f:
        for i in range(len(new_colors)):
            print("@define-color ", new_names[i]," #", new_colors[i],";", file=f, sep ='')
    with open(os.path.join(home,".config/colours/generated/colours.css"), "w") as f:
        print(":root{", file=f)
        for i in range(len(new_colors)):
            print("\t","--", new_names[i],":#", new_colors[i], file=f, sep='')
        print ("}", file=f)
    with open(os.path.join(home,".config/colours/generated/colours.conf"), "w") as f:
        for i in range(len(new_colors)):
                print("$", new_names[i],"=rgb(", new_colors[i],")", file=f, sep='')
    with open(os.path.join(home,".config/colours/generated/colours.rasi"), "w") as f:
        print("*{", file=f)
        for i in range(len(new_colors)):
                print("\t", new_names[i],":  #", new_colors[i],";", file=f, sep='')
        print ("}", file=f)

    # Move files
    for cursoftware in softList:
        if cursoftware["format"] != "search&replace":
            symlink = str("ln -sf ~/.config/colours/generated/" + cursoftware["format"] + " " + cursoftware["location"].replace("~", home) + "/" + cursoftware["format"])
            print(cursoftware["format"] + " " + cursoftware["location"] + "/")
            os.system(symlink)

        # The hard part    
        else:
            with open(cursoftware["location"].replace("~", home)+".template", "r+") as f:
                data = f.read()
                for i in range(len(colList)):
                    data = data.replace(new_names[i], new_colors[i])
            with open(cursoftware["location"].replace("~", home), 'w') as f:
                f.write(data)
    with open(home+"/.config/asexy/scripts/cache.json") as f:
        lines = f.readlines()
        lines[3] = '"colorscheme": "'+colorscheme.replace(".json","")+'"\n'
    with open(home+"/.config/asexy/scripts/cache.json", "w") as f:
        f.writelines(lines)

#Running the function
setcolors(colorscheme)

#Reload all necessary software
commands = json_load(os.path.join(home,".config/asexy/configs/commands.json"))
for i in commands:
    subprocess.call(i, shell=True)#Importing necessary modules
