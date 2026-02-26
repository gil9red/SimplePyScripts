#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/mozman/svgwrite/blob/master/examples/hyperlink.py


# pip install svgwrite
import svgwrite


def hyperlink(name, pretty) -> None:
    dwg = svgwrite.Drawing(name, (200, 200), debug=True)

    # use the hyperlink element
    link = dwg.add(dwg.a("http://www.w3.org"))
    link.add(dwg.ellipse(center=(100, 50), r=(50, 25), fill="red"))

    dwg.save(pretty=pretty)


if __name__ == "__main__":
    hyperlink("pretty_xml_in_svg_True.svg", pretty=True)
    hyperlink("pretty_xml_in_svg_False.svg", pretty=False)
