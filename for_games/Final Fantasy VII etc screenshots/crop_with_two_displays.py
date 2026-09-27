#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path

from PIL import Image

PATH_DIR: Path = Path(r"C:\Users\ipetrash\Desktop\FF7 Screenshots")
NAME_DIR_CROPPED: str = "cropped"


for path in PATH_DIR.rglob("*.*"):
    if path.suffix.lower() not in [".png", ".jpg", ".jpeg"]:
        continue

    path_img_cropped: Path = path.parent / NAME_DIR_CROPPED / path.name
    if path_img_cropped.exists():
        continue

    img = Image.open(path)
    width, height = img.size

    x1: int
    y1: int
    x2: int
    y2: int

    if width == 4480:  # Картинка на 2 экрана
        x1 = 1920
        y1 = 0
        x2 = width
        y2 = height

    elif width == 2560 and height == 1440:
        x1 = 0
        y1 = 30
        x2 = width
        y2 = 1390

    else:
        continue

    img_cropped = img.crop((x1, y1, x2, y2))
    crop_width, crop_height = img_cropped.size

    print(
        f"Cropping image {width}x{height} -> {crop_width}x{crop_height} "
        f'from "{path}" to "{path_img_cropped}"'
    )

    path_img_cropped.parent.mkdir(parents=True, exist_ok=True)
    img_cropped.save(path_img_cropped)
