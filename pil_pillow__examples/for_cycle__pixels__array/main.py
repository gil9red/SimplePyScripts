#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install Pillow
from PIL import Image


def get_pixel_array(img, rgb_hex=False):
    width, height = img.size

    pixels = []

    for y in range(height):
        row = []
        pixels.append(row)

        for x in range(width):
            r, g, b = img.getpixel((x, y))

            if rgb_hex:
                value = "{:02X}{:02X}{:02X}".format(r, g, b)
                row.append(value)
            else:
                row.append((r, g, b))

    return pixels


if __name__ == "__main__":
    img = Image.open("input.jpg")
    print(img)
    print()

    pixels = get_pixel_array(img)
    print("Rows: {}, cols: {}".format(len(pixels), len(pixels[0])))
    print([pixels[0][i] for i in range(2)])  # [(7, 7, 7), (23, 23, 23)]
    print()

    pixels = get_pixel_array(img, rgb_hex=True)
    print("Rows: {}, cols: {}".format(len(pixels), len(pixels[0])))
    print([pixels[0][i] for i in range(2)])  # ['070707', '171717']
