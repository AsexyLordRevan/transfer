import os
import json
import subprocess

home = os.environ["HOME"]

# Set working directory to Waybar config
waybar_config_path = os.path.join(home, ".config", "waybar")
os.chdir(waybar_config_path)

# Get list of theme directories
list_cmd = "ls -d */ | sed 's,/$,,'"
theme = subprocess.check_output(
    list_cmd + " | rofi -dmenu -p 'Theme?' -config ~/.config/rofi/script.rasi",
    shell=True
).decode("utf-8").strip()

print(f"Selected theme: {theme}")

# Restart waybar with selected theme
subprocess.call("killall waybar", shell=True)
subprocess.call(
    f"waybar -c '{waybar_config_path}/{theme}/config.jsonc' -s '{waybar_config_path}/{theme}/style.css' &",
    shell=True
)

# Path to the cache file
cache_path = os.path.join(home, ".config", "asexy", "scripts", "cache.json")

# Confirm the file exists
if not os.path.exists(cache_path):
    print(f"Error: Cache file not found at {cache_path}")
    exit(1)

# Load cache
try:
    with open(cache_path, "r") as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
    exit(1)

print("Original cache:", data)

# Update the waybar theme
data["waybar"] = theme

# Save updated cache
try:
    with open(cache_path, "w") as f:
        json.dump(data, f, indent=4)
    print("Cache updated successfully.")
except Exception as e:
    print(f"Error writing cache: {e}")
