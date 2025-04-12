#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/szabgab/slides/blob/914d15bb55cb0e335afcb72b6af0fa2aa9ed356f/python/examples/pil/draw_rectangle_with_rounded_corners.py


from PIL import Image, ImageDraw


Color = float | tuple[int, ...] | str


def round_corner(radius: int, fill: Color) -> Image:
    """Draw a round corner"""
    corner = Image.new("RGBA", (radius, radius), (0, 0, 0, 0))

    draw = ImageDraw.Draw(corner)
    draw.pieslice((0, 0, radius * 2, radius * 2), start=180, end=270, fill=fill)

    return corner


def round_rectangle(width: int, height: int, radius: int, fill: Color) -> Image:
    """Draw a rounded rectangle"""

    rectangle = Image.new("RGBA", (width, height), fill)
    corner = round_corner(radius, fill)

    rectangle.paste(corner, (0, 0))

    # Rotate the corner and paste it
    rectangle.paste(corner.rotate(90), (0, height - radius))

    rectangle.paste(corner.rotate(180), (width - radius, height - radius))
    rectangle.paste(corner.rotate(270), (width - radius, 0))

    return rectangle


if __name__ == "__main__":
    img = round_rectangle(width=500, height=500, radius=50, fill="yellow")
    img.show()
    img.save("img.png")
