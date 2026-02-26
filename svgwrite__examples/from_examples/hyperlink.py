#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/mozman/svgwrite/blob/master/examples/hyperlink.py


# pip install svgwrite
import svgwrite


def hyperlink(name) -> None:
    dwg = svgwrite.Drawing(name, (200, 200), debug=True)

    # use the hyperlink element
    link = dwg.add(dwg.a("http://www.w3.org"))
    link.add(dwg.ellipse(center=(100, 50), r=(50, 25), fill="red"))

    dwg.save(pretty=True)


if __name__ == "__main__":
    import sys

    prog_name = sys.argv[0].rstrip(".py") + ".svg"

    hyperlink(prog_name)
