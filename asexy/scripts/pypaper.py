import os
import subprocess
import json

home = os.environ['HOME']
wallpaper_dir = os.path.join(home, "Documents", "wallpapers")
rofi_config = os.path.expanduser("~/.config/rofi/icons.rasi")

os.chdir(os.path.join(home, ".config", "colours"))

# Get the selected wallpaper from rofi file browser
try:
    wlpr = subprocess.check_output(
        f"rofi -show filebrowser -config {rofi_config} -filebrowser-command 'echo' -modes filebrowser -filebrowser-directory {wallpaper_dir}/",
        shell=True
    ).decode("utf-8").strip()

    # Remove the base path part from the returned string
    wlpr = wlpr.replace(f"{wallpaper_dir}/", "")
    print(f"Selected wallpaper: {wlpr}")

except subprocess.CalledProcessError as e:
    print(f"Error running rofi: {e}")
    exit(1)

if not wlpr:
    print("No wallpaper selected, exiting")
    exit()

def set_wallpaper(wlpr):
    # Kill current wallpaper process
    subprocess.call("killall swaybg", shell=True)

    # Set the new wallpaper with swaybg
    wallpaper_path = os.path.join(wallpaper_dir, wlpr)
    subprocess.call(f"swww center img {wallpaper_path} &", shell=True)

    # Update the cache.json with the selected wallpaper
    cache_path = os.path.join(home, ".config", "asexy", "scripts", "cache.json")
    with open(cache_path, "r") as f:
        data = json.load(f)

    data["wallpaper"] = wlpr

    with open(cache_path, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Cache updated with wallpaper: {wlpr}")

# Set the wallpaper
set_wallpaper(wlpr)
