#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/mozman/svgwrite/blob/master/examples/solidcolor.py


# pip install svgwrite
import svgwrite


def solid_color(name) -> None:
    dwg = svgwrite.Drawing(name, size=("20cm", "15cm"), profile="tiny", debug=True)

    # set user coordinate space
    dwg.viewbox(width=200, height=150)
    dwg.add(dwg.circle((100, 100), 50, fill="red"))

    dwg.save()


if __name__ == "__main__":
    import sys

    prog_name = sys.argv[0].rstrip(".py") + ".svg"

    solid_color(prog_name)
