#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install Pillow
from PIL import Image
from PIL.Image import Resampling


def _resize_img(
    img: Image,
    width: int,
    height: int,
    resample: Resampling | None = None,
) -> Image:
    img_resized = img.resize(size=(width, height), resample=resample)
    img_resized.format = img.format  # NOTE: resize reset format
    return img_resized


def resize_height(
    img: Image,
    height: int,
    resample: Resampling | None = None,
) -> Image:
    """Resize by height, keep ratio."""
    return _resize_img(img, img.width * height // img.height, height, resample)


def resize_width(
    img: Image,
    width: int,
    resample: Resampling | None = None,
) -> Image:
    """Resize by width, keep ratio."""
    return _resize_img(img, width, img.height * width // img.width, resample)


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
