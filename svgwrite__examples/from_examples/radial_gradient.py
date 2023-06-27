#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/mozman/svgwrite/blob/master/examples/radialGradient.py


# pip install svgwrite
import svgwrite


def create_svg(name):
    dwg = svgwrite.Drawing(name, size=("20cm", "15cm"), profile="full", debug=True)

    # Ыet user coordinate space
    dwg.viewbox(width=200, height=150)

    # Create a new radialGradient element and add it to the defs section of the drawing
    gradient1 = dwg.defs.add(dwg.radialGradient())

    # Define the gradient from red to white
    gradient1.add_stop_color(0, "red").add_stop_color(1, "white")

    # Use gradient for filling the rect
    dwg.add(dwg.rect((10, 10), (50, 50), fill=gradient1.get_paint_server()))

    wave = dwg.defs.add(dwg.radialGradient())
    wave.add_colors(["blue", "lightblue"] * 8)
    dwg.add(dwg.rect((70, 10), (50, 50), fill=wave.get_paint_server()))

    dwg.save()


if __name__ == "__main__":
    import sys

    prog_name = sys.argv[0].rstrip(".py") + ".svg"

    create_svg(prog_name)
