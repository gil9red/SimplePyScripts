#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/mozman/svgwrite/blob/master/examples/ltattrie/color_triangles_function.py


import math

# pip install svgwrite
import svgwrite
from svgwrite import rgb


def create_svg(name):
    width = 900
    height = 900
    font_size = 20
    complete_size = 800  # size of the whole set of triangles.
    triangles_per_side = 50  # How many triangles there will be per side. integer.
    tri_height = math.sqrt(3) / 2.0

    title = "Example of creating your own colors."
    start = (
        (width - complete_size) / 2,
        (height - complete_size) / 2,
    )  # center triangle

    tri_color = ((20, 128, 30), (10, 0, 50), (0, 0, 128))
    dwg = svgwrite.Drawing(name, (width, height), debug=True)

    def draw_triangle(insert, size, fill, rotate=None):
        x, y = insert
        points = [insert, (x + size, y), ((x + size / 2.0), (y + size * tri_height))]
        triangle = dwg.add(dwg.polygon(points, fill=fill, stroke="none"))
        if rotate:
            triangle.rotate(rotate, center=insert)

    def nfrange(fstart, fstop, n):
        # n = number of points
        delta = (fstop - fstart) / n
        return [fstart + delta * i for i in range(n)]

    # Background will be dark but not black so the background does not overwhelm the colors.
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill="grey"))

    # Give the name of the example and a title.
    y = font_size + 5
    dwg.add(
        dwg.text(
            title, insert=(0, y), font_family="serif", font_size=font_size, fill="white"
        )
    )
    tri_size = complete_size / triangles_per_side
    tri_height = tri_size * tri_height
    ratio_side = nfrange(0.0, 1.0, triangles_per_side)

    for i in range(triangles_per_side, 0, -1):
        # The number of triangle in the row is the sum of the point up and the point down
        # triangles.
        num_tri_in_row = 2 * i - 1
        num_tri_drawn_in_row = 0

        # Calculate color
        start_color = [
            int(
                tri_color[0][k] * ratio_side[i - 1]
                + tri_color[2][k] * (1 - ratio_side[i - 1])
            )
            for k in range(3)
        ]
        end_color = [
            int(
                tri_color[1][k] * ratio_side[i - 1]
                + tri_color[2][k] * (1 - ratio_side[i - 1])
            )
            for k in range(3)
        ]

        # Calculate ratios of the two ending colors.
        ratio_row = nfrange(0.0, 1.0, num_tri_in_row) if num_tri_in_row > 1 else [0.5]

        for j in range(i):
            x = start[0] + (j + ((triangles_per_side - i) / 2.0)) * tri_size
            y = start[1] + (triangles_per_side - i) * tri_height
            # Calculate color
            new_color = [
                int(
                    start_color[k] * (1 - ratio_row[num_tri_drawn_in_row])
                    + end_color[k] * ratio_row[num_tri_drawn_in_row]
                )
                for k in range(3)
            ]
            draw_triangle((x, y), tri_size, rgb(*new_color))
            num_tri_drawn_in_row += 1

            if j != i - 1:
                # The on screen point up triangles have one fewer per row.
                x += tri_size

                # Calculate color
                new_color = [
                    int(
                        start_color[k] * (1 - ratio_row[num_tri_drawn_in_row])
                        + end_color[k] * ratio_row[num_tri_drawn_in_row]
                    )
                    for k in range(3)
                ]
                draw_triangle((x, y), tri_size, rgb(*new_color), rotate=60)
                num_tri_drawn_in_row += 1

    dwg.save()


if __name__ == "__main__":
    import sys

    prog_name = sys.argv[0].rstrip(".py") + ".svg"

    create_svg(prog_name)
