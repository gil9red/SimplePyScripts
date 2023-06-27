#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install svgwrite
import svgwrite


def create_svg(name):
    svg_size_width = 200
    svg_size_height = 200

    dwg = svgwrite.Drawing(name, (svg_size_width, svg_size_height), debug=True)

    # Background will be black so the background does not overwhelm the colors.
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill="black"))

    dwg.add(dwg.rect(insert=("25%", "25%"), size=("50%", "50%"), fill="yellow"))

    dwg.save()


if __name__ == "__main__":
    import sys

    prog_name = sys.argv[0].rstrip(".py") + ".svg"

    create_svg(prog_name)
