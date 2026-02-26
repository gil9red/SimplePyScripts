#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/mozman/svgwrite/blob/master/examples/pattern.py


# pip install svgwrite
import svgwrite


def create_svg(name) -> None:
    dwg = svgwrite.Drawing(name, size=("20cm", "15cm"), profile="full", debug=True)

    # Set user coordinate space
    dwg.viewbox(width=200, height=150)

    pattern = dwg.defs.add(dwg.pattern(size=(20, 20), patternUnits="userSpaceOnUse"))
    pattern.add(dwg.circle((10, 10), 5))
    dwg.add(dwg.circle((100, 100), 50, fill=pattern.get_paint_server()))

    dwg.save()


if __name__ == "__main__":
    import sys

    prog_name = sys.argv[0].rstrip(".py") + ".svg"

    create_svg(prog_name)
