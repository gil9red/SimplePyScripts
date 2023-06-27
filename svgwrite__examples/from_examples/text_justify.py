#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/mozman/svgwrite/blob/master/examples/ltattrie/text_justify.py


# pip install svgwrite
import svgwrite


def create_svg(name):
    svg_size = 900
    font_size = 20
    title = "Example of text_anchor (justified) text"
    dwg = svgwrite.Drawing(name, (svg_size, svg_size), debug=True)

    # Background will be white.
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill="white"))

    # Give the name of the example and a title.
    dwg.add(
        dwg.text(
            title,
            insert=(0, (font_size + 5)),
            font_family="serif",
            font_size=font_size,
            fill="black",
        )
    )

    # Show default
    dwg.add(
        dwg.text(
            "No specified text_anchor means 'start' justified text",
            insert=("50%", font_size * 3),
            font_family="sans-serif",
            font_size=font_size,
            fill="black",
        )
    )

    # Add a circle to show the anchor point printing on top of the text.
    dwg.add(dwg.circle(("50%", font_size * 3), r="3px", fill="red"))

    for i, anchor in enumerate(
        ["start", "end", "middle"]
    ):  # also 'inherit' which inherits from parent.
        dwg.add(
            dwg.text(
                "text_anchor='" + anchor + "' means " + anchor + " justified text",
                insert=("50%", font_size * (i + 4)),
                text_anchor=anchor,
                font_family="sans-serif",
                font_size=font_size,
                fill="black",
            )
        )

        # Add a circle to show the anchor point printing on top of the text.
        dwg.add(dwg.circle(("50%", font_size * (i + 4)), r="3px", fill="red"))

    dwg.save()


if __name__ == "__main__":
    import sys

    prog_name = sys.argv[0].rstrip(".py") + ".svg"

    create_svg(prog_name)
