#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install Pillow
from PIL import Image
from PIL.Image import Resampling


# SOURCE: https://stackoverflow.com/a/77470620/5909792


def resize_height(img: Image, height: int, resample: int | None = None) -> Image:
    """Resize by height, keep ratio."""
    return img.resize((img.width * height // img.height, height), resample=resample)


def resize_width(img: Image, width: int, resample: int | None = None) -> Image:
    """Resize by width, keep ratio."""
    return img.resize((width, img.height * width // img.width), resample=resample)


if __name__ == "__main__":
    file_name = "input.jpg"
    img = Image.open(file_name)
    print(img.size)
    # (660, 438)

    resample = Resampling.LANCZOS

    img_height_300 = resize_height(img, height=300, resample=resample)
    img_height_300.save("output_height=300.jpg")
    print(img_height_300.size)
    # (452, 300)

    img_width_300 = resize_width(img, width=300, resample=resample)
    img_width_300.save("output_width=300.jpg")
    print(img_width_300.size)
    # (300, 199)
