#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/szabgab/slides/blob/914d15bb55cb0e335afcb72b6af0fa2aa9ed356f/python/examples/pil/draw_rectangle_with_rounded_corners.py


# TODO: append alpha


from PIL import Image, ImageDraw


def round_corner(radius, fill):
    """Draw a round corner"""
    corner = Image.new("RGB", (radius, radius), (0, 0, 0, 0))
    draw = ImageDraw.Draw(corner)
    draw.pieslice((0, 0, radius * 2, radius * 2), 180, 270, fill=fill)
    return corner


def round_rectangle(size, radius, fill):
    """Draw a rounded rectangle"""
    width, height = size
    rectangle = Image.new("RGBA", size, fill)
    corner = round_corner(radius, fill)

    rectangle.paste(corner, (0, 0))

    # Rotate the corner and paste it
    rectangle.paste(corner.rotate(90), (0, height - radius))

    rectangle.paste(corner.rotate(180), (width - radius, height - radius))
    rectangle.paste(corner.rotate(270), (width - radius, 0))
    return rectangle


img = round_rectangle((500, 500), 50, "yellow")
img.show()
img.save("img.png")
