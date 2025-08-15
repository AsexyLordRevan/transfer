import argparse
from PIL import Image, ImageDraw
import math
import statistics
import os
import json
import colorsys

parser = argparse.ArgumentParser(description="Extract color palette from an image and create a PNG preview.")
parser.add_argument("image_path", type=str, help="Path to the image file")
args = parser.parse_args()

image = Image.open(args.image_path).convert("RGB")
pixels = image.load()
width, height = image.size

dark, light = [], []
black_list, white_list, grey_list = [], [], []
red_list, orange_list, yellow_list, green_list, blue_list, mauve_list = [], [], [], [], [], []

def rgb_to_hsv(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return round(h * 360, 0), round(s * 100, 0), round(v * 100, 0)

def sort_col(hsv):
    h, s, v = hsv
    if v < 35:
        black_list.append(hsv)
    elif v > 85:
        white_list.append(hsv)
    elif s < 30:
        grey_list.append(hsv)
    elif (0 <= h <= 15) or (320 <= h <= 360):
        red_list.append(hsv)
    elif 15 < h <= 35:
        orange_list.append(hsv)
    elif 35 < h <= 50:
        yellow_list.append(hsv)
    elif 60 < h <= 150:
        green_list.append(hsv)
    elif 150 < h <= 260:
        blue_list.append(hsv)
    elif 260 < h < 320:
        mauve_list.append(hsv)

def calculate_avg(color_list):
    if not color_list:
        return [0, 0, 0]
    sum_x = sum(math.cos(math.radians(h[0])) for h in color_list)
    sum_y = sum(math.sin(math.radians(h[0])) for h in color_list)
    avg_hue = math.degrees(math.atan2(sum_y, sum_x)) % 360
    avg_saturation = statistics.fmean([h[1] for h in color_list])
    avg_value = statistics.fmean([h[2] for h in color_list])
    return [avg_hue / 360, avg_saturation / 100, avg_value / 100]

def rgb_to_hex(rgb):
    return '{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

def extract_colors():
    colors = {
        "bg1": calculate_avg(grayscale_list[2*len(grayscale_list)//3:]),
        "txt": calculate_avg(white_list if white_list else grey_list),
        "st1": calculate_avg(grey_list if grey_list else black_list),
        "st2": calculate_avg(black_list if black_list else grey_list),
        "st3": calculate_avg(black_list),
        "red": calculate_avg(red_list),
        "orange": calculate_avg(orange_list),
        "yellow": calculate_avg(yellow_list),
        "white": calculate_avg(white_list),
        "green": calculate_avg(green_list),
        "blue": calculate_avg(blue_list),
        "mauve": calculate_avg(mauve_list)
    }
    for key, hsv in colors.items():
        rgb = colorsys.hsv_to_rgb(*hsv)
        rgb = [round(c * 255) for c in rgb]
        colors[key] = rgb_to_hex(rgb)
    return colors

def output_colors(image_path):
    colors = extract_colors()
    for key, value in colors.items():
        print(f"{key}: #{value}")
    output_directory = os.path.expanduser("~/.config/colours/colorschemes/")
    os.makedirs(output_directory, exist_ok=True)
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    output_path = os.path.join(output_directory, f"{image_name}.json")
    with open(output_path, "w") as file:
        json.dump(colors, file, indent=4)
    print(f"Color scheme saved to {output_path}")

for y in range(height):
    for x in range(width):
        rgb = pixels[x, y]
        hsv = rgb_to_hsv(*rgb[:3])
        if hsv[2] > 50:
            light.append(hsv[2])
        else:
            dark.append(hsv[2])
        sort_col(hsv)

if len(light) > len(dark):
    print("The image is light")
else:
    print("The image is dark")

grayscale_list = sorted(black_list + white_list + grey_list, key=lambda x: x[2])

output_colors(args.image_path)
