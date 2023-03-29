""" Based on a source image, create a new image with a black background and white circles

Usage: python3 circle_image.py <'random' or 'grid'> <input_image_path> <output_image_path>



"""


from enum import Enum
from PIL import Image, ImageDraw, ImageOps
import numpy as np
import sys

# Constants
MIN_DISTANCE = 40  # If less than MAX_SIZE, circles will overlap
MIN_SIZE = 5
MAX_SIZE = 30
NUM_CIRCLES = 10000  # Relevant only for randomly placed circles

class Type(Enum):
    RANDOM = 1
    GRID = 2

def generate_circles_random(width, height, brightness_data, num_circle_attempts):
    circles = []
    for _ in range(num_circle_attempts):
        x = np.random.randint(0, width)
        y = np.random.randint(0, height)
        brightness_value = brightness_data[y, x]

        size = int(MIN_SIZE + brightness_value * (MAX_SIZE - MIN_SIZE))

        circle = (x, y, size)

        if not any(distance(circle, c) < MIN_DISTANCE + (size + c[2]) / 2 for c in circles):
            circles.append(circle)

    return circles

def generate_circles_grid(width, height, brightness, min_distance):
    circles = []
    offset_y = min_distance // 2
    for y in range(0, height, min_distance):
        offset_x = min_distance // 2 if (y // min_distance) % 2 == 1 else 0
        for x in range(offset_x, width, min_distance):
            brightness_value = brightness[y, x]

            size = int(MIN_SIZE + brightness_value * (MAX_SIZE - MIN_SIZE))

            circle = (x, y, size)
            circles.append(circle)

    return circles

def distance(circle1, circle2):
    x1, y1, _ = circle1
    x2, y2, _ = circle2
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def draw_circles(img, circles):
    draw = ImageDraw.Draw(img)
    for x, y, size in circles:
        draw.ellipse((x - size // 2, y - size // 2, x + size // 2, y + size // 2), fill=(255, 255, 255))

def main(type: Type, input_path, output_path):
    source_image = Image.open(input_path).convert("RGB")
    output_image = Image.new("RGB", source_image.size, "black")

    width, height = source_image.size
    source_grayscale = source_image.convert("L")
    source_brightness = np.array(source_grayscale) / 255

    circles = []
    if type == Type.RANDOM:
        circles = generate_circles_random(width, height, source_brightness, NUM_CIRCLES)
    else:
        circles = generate_circles_grid(width, height, source_brightness, MIN_DISTANCE)
    print(len(circles))
    draw_circles(output_image, circles)

    output_image.save(output_path)

if __name__ == "__main__":
    if len(sys.argv) != 4 or sys.argv[1] not in ["random", "grid"]:
        print("Usage: python3 circle_image.py <random or grid> <input_image_path> <output_image_path>")
    else:
        main(Type[sys.argv[1].upper()], sys.argv[2], sys.argv[3])
