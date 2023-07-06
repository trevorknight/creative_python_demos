""" Based on a source image, create a new image with a black background and white circles

The circles are either randomly placed or placed in a grid pattern.  Their size is proportional
to the brightness at their location.

Usage: python3 circle_image.py <random or grid> <input_image_path> <output_image_path>
"""


import sys
from dataclasses import dataclass
from enum import Enum
from math import sqrt

import numpy as np
from PIL import Image, ImageDraw

# Constants
MIN_DISTANCE = 1
MIN_SIZE = 1
MAX_SIZE = 10
# Relevant only for randomly placed circles.  In practice, this is
# the number of attempted circles, as circles closer than MIN_DISTANCE
# will be rejected.
NUM_CIRCLES = 10000


class Type(Enum):
    RANDOM = 1
    GRID = 2


@dataclass
class Circle:
    x: int
    y: int
    radius: int


def generate_circles_random(
    width, height, brightness_data, num_circle_attempts
) -> list[Circle]:
    circles: list[Circle] = []
    for _ in range(num_circle_attempts):
        x = np.random.randint(0, width)
        y = np.random.randint(0, height)
        brightness_value = brightness_data[y, x]
        # Radius is proprotional to brightness of the original
        radius = int(MIN_SIZE + brightness_value * (MAX_SIZE - MIN_SIZE) / 2)
        circle = Circle(x, y, radius)
        # Woof, this is inefficient.
        if not any(distance(circle, c) < MIN_DISTANCE for c in circles):
            circles.append(circle)

    return circles


def generate_circles_grid(width, height, brightness, grid_distance) -> list[Circle]:
    circles: list[Circle] = []
    offset_y = grid_distance // 2
    for y in range(0, height, grid_distance):
        # Every other row is offset by half a grid distance to make more of a checkerboard pattern.
        offset_x = grid_distance // 2 if (y // grid_distance) % 2 == 1 else 0
        for x in range(offset_x, width, grid_distance):
            brightness_value = brightness[y, x]
            # Radius is proprotional to brightness of the original
            radius = int(MIN_SIZE + brightness_value * (MAX_SIZE - MIN_SIZE) / 2)
            circle = Circle(x, y, radius)
            circles.append(circle)

    return circles


def distance(c1, c2):
    """Distance between the outer edges of two circles."""
    return sqrt((c1.x - c2.x) ** 2 + (c1.y - c2.y) ** 2) - c1.radius - c2.radius


def draw_circles(img, circles):
    draw = ImageDraw.Draw(img)
    for c in circles:
        draw.ellipse(
            (c.x - c.radius, c.y - c.radius, c.x + c.radius, c.y + c.radius),
            fill=(255, 255, 255),
        )


def main(type: Type, input_path, output_path):
    source_image = None
    with Image.open(input_path) as source:
        source_image = source.convert("L")  # "L" converts to grayscale

    width, height = source_image.size
    # Create brightness on a [0, 1] scale.
    source_brightness = np.array(source_image) / 255

    circles: list[Circle] = []
    if type == Type.RANDOM:
        circles = generate_circles_random(width, height, source_brightness, NUM_CIRCLES)
    else:
        circles = generate_circles_grid(
            width, height, source_brightness, MAX_SIZE + MIN_DISTANCE
        )
    # I'm curious how many circles we actually get (especially for the random method).
    print(f"Total circles: {len(circles)}")

    with Image.new("RGB", source_image.size, "black") as output_image:
        draw_circles(output_image, circles)
        output_image.save(output_path)


if __name__ == "__main__":
    if len(sys.argv) != 4 or sys.argv[1] not in ["random", "grid"]:
        print(
            "Usage: python3 circle_image.py <random or grid> <input_image_path> <output_image_path>"
        )
    else:
        main(Type[sys.argv[1].upper()], sys.argv[2], sys.argv[3])
