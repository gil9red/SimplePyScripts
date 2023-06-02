#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install Pillow
from PIL import Image, ImageDraw


def draw_progress(image: Image, percent: int) -> Image:
    if percent < 0:
        return image

    if percent > 100:
        percent = 100

    width, height = image.size

    progress_width = width * (percent / 100)
    progress_height = height * (10 / 100)  # Пусть будет 10% от высоты

    x0 = 0
    y0 = height * (80 / 100)  # 80% от высоты
    x1 = x0 + progress_width
    y1 = y0 + progress_height

    image = image.copy()

    drawer = ImageDraw.Draw(image)
    drawer.rectangle(xy=[x0, y0, x1, y1], fill=(0, 255, 0))  # RGB, green

    return image


if __name__ == "__main__":
    image_file = "input.jpg"
    image = Image.open(image_file)

    for percent in (5, 15, 75, 100):
        img = draw_progress(image, percent)
        img.save(f"output/image_{percent}%.png")
        img.show()
