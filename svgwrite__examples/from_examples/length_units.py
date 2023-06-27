#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/mozman/svgwrite/blob/master/examples/ltattrie/length_units.py


# pip install svgwrite
import svgwrite


def create_svg(name):
    svg_size = 900
    font_size = 20
    title1 = "Example of units of length"
    title2 = "Example of class Unit and import from svgwrite cm, mm"

    sample = (
        (
            "px", " one user unit which may or may not be pixels. This is the default if no units are specified.",
        ),
        ("pt", " 1.25px."),
        ("mm", " 3.543307px."),
        ("ex", " the current font's height of the character x."),
        ("%", " percent of the size of the viewport."),
        ("pc", " 15px."),
        ("em", " the current font's height."),
        ("cm", " 35.43307px."),
        ("in", " 90px."),
    )

    dwg = svgwrite.Drawing(name, (svg_size, svg_size))

    # Background will be white.
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill="white"))

    # Give the name of the example and a title.
    y = font_size + 5
    x = 5
    line_space = font_size * 2

    group = dwg.add(dwg.g(font_family="serif", font_size=font_size, fill="black"))
    group.add(dwg.text(title1, insert=(x, y)))

    for i, sample_item in enumerate(sample):
        y += line_space
        unit = sample_item[0]
        group.add(dwg.rect(insert=(0, y), size=("1" + unit, "3px"), fill="red"))
        group.add(dwg.text("size='1%s': %s" % sample_item, insert=("2in", y + 3)))

    # Show the use of class Unit
    y += line_space

    text_lines = (
        title2,
        "The Unit class overrides the right hand multiply",
        '2*3*cm returns the string "6cm"',
    )

    for txt in text_lines:
        group.add(dwg.text(txt, insert=(x, y)))
        y += line_space

    dwg.save()


if __name__ == "__main__":
    import sys

    prog_name = sys.argv[0].rstrip(".py") + ".svg"

    create_svg(prog_name)
