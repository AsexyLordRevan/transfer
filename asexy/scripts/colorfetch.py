import os
import json

def hex_to_rgb(hex_color):
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return r, g, b

# Define the EndeavourOS ASCII logo (6 lines)
eos_logo = [
    "     /\\     ",
    "    //  \\   ",
    "   //    \ \ ",
    " / /     _) )",
    "/_/___-- __- ",
    "  /____--    "
]

home = os.path.expanduser("~")

# Load colorscheme name
with open(f"{home}/.config/asexy/scripts/cache.json") as f:
    colorscheme = json.load(f)["colorscheme"]

# Load colors
with open(f"{home}/.config/colours/colorschemes/{colorscheme}.json") as f:
    colors = list(json.load(f).values())

# Generate colored blocks
blocks = []
for hex_color in colors:
    r, g, b = hex_to_rgb(hex_color)
    block = f"\033[48;2;{r};{g};{b}m   \033[0m"
    blocks.append(block)

# Split blocks into two lines
line1 = " ".join(blocks[:7])
line2 = " ".join(blocks[7:14])

# Print output
print(f"{eos_logo[0]}  {line1}")
print(f"{eos_logo[1]}  {line2}")
for i in range(2, 6):
    print(eos_logo[i])
