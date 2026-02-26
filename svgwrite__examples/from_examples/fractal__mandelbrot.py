#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/mozman/svgwrite/blob/master/examples/mandelbrot.py


# pip install svgwrite
import svgwrite
from svgwrite import rgb


# SOURCE: http://code.activestate.com/recipes/577111/
def create_svg(name) -> None:
    # Mandelbrot fractal
    # FB - 201003254

    def put_pixel(pos, color) -> None:
        mandelbrot_group.add(dwg.circle(center=pos, r=0.5, fill=color))

    # Image size
    imgx = 160
    imgy = 100

    # Drawing defines the output size
    dwg = svgwrite.Drawing(name, ("32cm", "20cm"), debug=True)

    # Define a user coordinate system with viewbox()
    dwg.viewbox(0, 0, imgx, imgy)

    mandelbrot_group = dwg.add(dwg.g(stroke_width=0, stroke="none"))

    # Drawing area
    xa = -2.0
    xb = 1.0
    ya = -1.5
    yb = 1.5
    max_it = 255  # Max iterations allowed

    for y in range(imgy):
        zy = y * (yb - ya) / (imgy - 1) + ya
        for x in range(imgx):
            zx = x * (xb - xa) / (imgx - 1) + xa
            z = zx + zy * 1j
            c = z

            for i in range(max_it):
                if abs(z) > 2.0:
                    break

                z = z * z + c

            put_pixel((x, y), rgb(i % 4 * 64, i % 8 * 32, i % 16 * 16))

    dwg.save()


if __name__ == "__main__":
    import sys

    prog_name = sys.argv[0].rstrip(".py") + ".svg"

    create_svg(prog_name)
