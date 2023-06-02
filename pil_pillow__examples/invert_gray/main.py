#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install Pillow
from PIL import Image, ImageOps


def invert(image):
    if image.mode == "RGBA":
        r, g, b, a = image.split()
        rgb_image = Image.merge("RGB", (r, g, b))
        inverted_image = ImageOps.invert(rgb_image)
        r2, g2, b2 = inverted_image.split()
        return Image.merge("RGBA", (r2, g2, b2, a))

    else:
        return ImageOps.invert(image)


if __name__ == "__main__":
    image_file = "input.jpg"
    image = Image.open(image_file)

    image_invert = invert(image)
    image_invert_gray = ImageOps.grayscale(image_invert)
    image_invert_gray.save("image_invert_gray.png")
    image_invert_gray.show()
