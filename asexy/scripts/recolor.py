import argparse
import json
import math
import os
from PIL import Image

# ----- Arguments ----- #
parser = argparse.ArgumentParser(description="Recolor an image using the closest color from a JSON hex palette.")
parser.add_argument("image_path", type=str, help="Path to the image file")
parser.add_argument("colors", type=str, help="Path to the JSON file with hex colors")
args = parser.parse_args()

# ----- Load image ----- #
image = Image.open(args.image_path).convert("RGB")
pixels = image.load()
width, height = image.size

# ----- Load and convert hex colors to RGB ----- #
with open(args.colors, "r") as file:
    hex_colors = json.load(file)

palette = []
for hexcolor in hex_colors.values():
    hexcolor = hexcolor.lstrip('#')
    r = int(hexcolor[0:2], 16)
    g = int(hexcolor[2:4], 16)
    b = int(hexcolor[4:6], 16)
    palette.append((r, g, b))

# ----- Function to find closest color ----- #
def closest_color(curr_color):
    min_dist = float('inf')
    closest = None
    for color in palette:
        dist = math.sqrt(
            (curr_color[0] - color[0])**2 +
            (curr_color[1] - color[1])**2 +
            (curr_color[2] - color[2])**2
        )
        if dist < min_dist:
            min_dist = dist
            closest = color
    return closest

# ----- Recolor image ----- #
new_image = Image.new("RGB", (width, height))
for x in range(width):
    for y in range(height):
        original_color = pixels[x, y]
        new_color = closest_color(original_color)
        new_image.putpixel((x, y), new_color)

# ----- Save in same directory ----- #
base_name = os.path.splitext(os.path.basename(args.image_path))[0]
directory = os.path.dirname(args.image_path)
output_path = os.path.join(directory, f"{base_name}_recolored.png")
new_image.save(output_path)
print(f"✅ Saved recolored image to: {output_path}")
