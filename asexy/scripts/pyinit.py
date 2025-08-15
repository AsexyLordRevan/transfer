#!/usr/bin/env python3

import json
from subprocess import Popen
from pathlib import Path

cache = json.load(open(Path(__file__).parent / "cache.json"))
home = Path.home()

if wp := cache.get("wallpaper"):
    Popen(["swaybg", "-i", f"{home}/Documents/wallpapers/{wp}"])

if wb := cache.get("waybar"):
    Popen([
        "waybar",
        "-c", f"{home}/.config/waybar/{wb}/config.jsonc",
        "-s", f"{home}/.config/waybar/{wb}/style.css"
    ])
