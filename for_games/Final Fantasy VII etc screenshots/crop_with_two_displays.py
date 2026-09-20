#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path

from PIL import Image

PATH_DIR: Path = Path(r"C:\Users\ipetrash\Desktop\FF7 Screenshots")
PATH_DIR_CROPPED: Path = PATH_DIR / "cropped"


for path in PATH_DIR.rglob("*.*"):
    if path.suffix.lower() not in [".png", ".jpg", ".jpeg"]:
        continue

    path_img_cropped: Path = PATH_DIR_CROPPED / path.name
    if path_img_cropped.exists():
        continue

    img = Image.open(path)
    width, height = img.size
    if width <= 2560:
        continue

    if width == 4480:
        x1 = 1920
        y1 = 0
        x2 = width
        y2 = height

        img_cropped = img.crop((x1, y1, x2, y2))
        crop_width, crop_height = img_cropped.size

        print(
            f"Cropping image {width}x{height} -> {crop_width}x{crop_height} "
            f'from "{path}" to "{path_img_cropped}"'
        )

        path_img_cropped.parent.mkdir(parents=True, exist_ok=True)
        img_cropped.save(path_img_cropped)

        continue
