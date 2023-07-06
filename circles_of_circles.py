""" Draws a series of concentric rings, each made up of small circles.

A bad drawing but you get the idea:
          .
      .       .
    .    . .    .
   .   .     .   .
    .    . .    .
      .       .
          .


This is designed to be used with Inkscape python extension.

"Rings" are the larger circles, and "circles" are the smaller circles that make up the rings.

"""

import math


def draw_circles_of_circles(
    center_x,
    center_y,
    starting_ring_radius,
    final_ring_radius,
    starting_circle_size,
    final_circle_size,
    circles_per_ring,
    num_rings,
):
    circle_size_step = (starting_circle_size - final_circle_size) / (num_rings - 1)

    # Calculate total size of all "slots"
    total_slot_size = sum(
        [starting_circle_size - i * circle_size_step for i in range(num_rings)]
    )

    # Calculate scaling factor for slot sizes
    slot_size_scale = (starting_ring_radius - final_ring_radius) / total_slot_size

    ring_radius = starting_ring_radius
    circle_size = starting_circle_size

    for ring in range(num_rings):
        for circ in range(circles_per_ring):
            # Calculate the angle for this circle
            angle = circ * 2 * math.pi / circles_per_ring

            # If the ring number is odd, add an offset to the angle to stagger the circles
            if ring % 2 == 1:
                angle += math.pi / circles_per_ring

            # Calculate the x and y coordinates for this circle
            x = center_x + ring_radius * math.cos(angle)
            y = center_y + ring_radius * math.sin(angle)

            # Draw the circle.  This is a method in the Inkscape python extension.
            circle((x, y), circle_size)

        # After drawing all the circles in the ring, calculate the size for next ring's circles
        if ring != num_rings - 1:  # Skip for the last ring
            next_circle_size = circle_size - circle_size_step

            # Calculate ring radius step based on average circle size
            ring_radius_step = (circle_size + next_circle_size) / 2 * slot_size_scale
            ring_radius -= ring_radius_step

            circle_size = next_circle_size


center_x = 528 / 2
center_y = 48 + 528 / 2

starting_ring_radius = 225
final_ring_radius = 100

starting_circle_size = 15
final_circle_size = 5

circles_per_ring = 36

num_rings = 5

draw_circles_of_circles(
    center_x=center_x,
    center_y=center_y,
    starting_ring_radius=starting_ring_radius,
    final_ring_radius=final_ring_radius,
    starting_circle_size=starting_circle_size,
    final_circle_size=final_circle_size,
    circles_per_ring=circles_per_ring,
    num_rings=num_rings,
)


starting_ring_radius = 100
final_ring_radius = 8

starting_circle_size = 12
final_circle_size = 3

circles_per_ring = 18


draw_circles_of_circles(
    center_x=center_x,
    center_y=center_y,
    starting_ring_radius=starting_ring_radius,
    final_ring_radius=final_ring_radius,
    starting_circle_size=starting_circle_size,
    final_circle_size=final_circle_size,
    circles_per_ring=circles_per_ring,
    num_rings=num_rings,
)
