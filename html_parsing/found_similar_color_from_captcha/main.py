#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re

from base64 import b64decode
from io import BytesIO

from bs4 import BeautifulSoup
from PIL import Image


PATTERN_BACKGROUND_IMAGE = re.compile(
    r"background-image: url\(data:image/\w+;base64,(.+)\)"
)


def get_rgb(style: str) -> tuple[int, int, int]:
    m = PATTERN_BACKGROUND_IMAGE.search(style)
    if not m:
        raise Exception("Не удалось найти background-image!")

    img_base64 = m.group(1).encode("utf-8")
    img_data = b64decode(img_base64)

    # Приводим к RGB, т.к. одновременно встречались разные цвета: RGB, RGBA, LA
    img = Image.open(BytesIO(img_data)).convert("RGB")

    # Картинки имеют однородный цвет
    return img.getpixel((0, 0))


def pixel_matches_color(
    rgb1: tuple[int, int, int],
    rgb2: tuple[int, int, int],
    tolerance: int = 20,
) -> bool:
    r, g, b = rgb1
    ex_r, ex_g, ex_b = rgb2
    return (
        (abs(r - ex_r) <= tolerance)
        and (abs(g - ex_g) <= tolerance)
        and (abs(b - ex_b) <= tolerance)
    )


soup = BeautifulSoup(open("rutor.live.htm", encoding="utf-8"), "html.parser")

target_el = soup.select_one('#content > div[style*="background-image"]')
target_rgb = get_rgb(target_el["style"])
print("target_rgb:", target_rgb)
# target_rgb: (1, 9, 254)

for variant_el in soup.select('#content em[style*="background-image"]'):
    variant_rgb = get_rgb(variant_el["style"])
    print("variant_rgb:", variant_rgb, pixel_matches_color(variant_rgb, target_rgb))
"""
variant_rgb: (255, 0, 0) False
variant_rgb: (255, 255, 0) False
variant_rgb: (0, 128, 0) False
variant_rgb: (0, 0, 0) False
variant_rgb: (128, 128, 128) False
variant_rgb: (0, 0, 255) True
"""
