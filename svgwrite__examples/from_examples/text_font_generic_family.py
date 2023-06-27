#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/mozman/svgwrite/blob/master/examples/ltattrie/text_font_generic_family.py

# pip install svgwrite
import svgwrite


# http://www.w3.org/TR/2008/REC-CSS2-20080411/fonts.html#propdef-font-family
# 'serif', 'sans-serif', 'cursive', 'fantasy', and 'monospace' from the CSS specification


def create_svg(name):
    font_size = 20
    title = name + ": Example of text using generic family fonts"

    font_family_sample = (
        ("serif", "have finishing strokes, flared or tapering ends."),
        ("sans-serif", "have stroke endings that are plain."),
        ("cursive", "the characters are partially or completely connected"),
        ("fantasy", " primarily decorative characters."),
        ("monospace", "all characters have the same fixed width."),
    )

    dwg = svgwrite.Drawing(name, debug=True)

    # background will be white.
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill="white"))

    # give the name of the example and a title.
    dwg.add(
        dwg.text(
            title,
            insert=(0, (font_size + 5)),
            font_family="serif",
            font_size=font_size,
            fill="black",
        )
    )

    for i, (font, text) in enumerate(font_family_sample):
        dwg.add(
            dwg.text(
                "font_family='" + font + "': " + text,
                insert=(font_size, font_size * (i * 2 + 4)),
                font_family=font,
                font_size=font_size,
                fill="black",
            )
        )

    dwg.save()


if __name__ == "__main__":
    import sys

    prog_name = sys.argv[0].rstrip(".py") + ".svg"

    create_svg(prog_name)
