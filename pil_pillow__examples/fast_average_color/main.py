#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import math
from pathlib import Path

from PIL import Image


DIR = Path(__file__).resolve().parent


def get_mode_correction(image: Image) -> str:
    if image.mode not in ["RGB", "RGBA"]:
        return "RGB"
    return image.mode


# SOURCE: https://github.com/fast-average-color/fast-average-color/blob/15561aa55a36702f0b1af3d0ef611a205f8d56b5/src/algorithm/sqrt.js#L3
def sqrt_algorithm(image: Image) -> tuple[int, int, int, int]:
    mode = get_mode_correction(image)
    if mode != image.mode:
        image = image.convert("RGB")

    red_total = 0
    green_total = 0
    blue_total = 0
    alpha_total = 0
    count = 0

    pixel = image.load()

    for i in range(image.width):
        for j in range(image.height):
            color = pixel[i, j]
            if len(color) == 4:
                red, green, blue, alpha = color
            else:
                [red, green, blue], alpha = color, 255

            red_total += red * red * alpha
            green_total += green * green * alpha
            blue_total += blue * blue * alpha
            alpha_total += alpha

            count += 1

    return (
        round(math.sqrt(red_total / alpha_total)),
        round(math.sqrt(green_total / alpha_total)),
        round(math.sqrt(blue_total / alpha_total)),
        round(alpha_total / count),
    )


def draw_example(image: Image, margin=70) -> Image:
    rgba = sqrt_algorithm(image)

    width = image.width + margin + margin
    height = image.height + margin + margin

    mode = get_mode_correction(image)

    image_output = Image.new(mode, (width, height), rgba)
    image_output.paste(image, (margin, margin))

    return image_output


if __name__ == "__main__":
    for file_name in DIR.glob("input/*.*"):
        image = Image.open(file_name)
        image_output = draw_example(image)
        # image_output.show()
        image_output.save(DIR / "output" / file_name.name)
