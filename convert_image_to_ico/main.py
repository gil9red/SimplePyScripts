#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PIL import Image


def convert_image_to_ico(file_name, file_name_ico, icon_sizes=None) -> None:
    img = Image.open(file_name)

    if icon_sizes:
        img.save(file_name_ico, sizes=icon_sizes)
    else:
        img.save(file_name_ico)


if __name__ == "__main__":
    file_name = "image.jpg"

    convert_image_to_ico(file_name, "logo.ico")
    convert_image_to_ico(
        file_name,
        "logo2.ico",
        icon_sizes=[(16, 16), (32, 32), (48, 48), (64, 64)],
    )
    convert_image_to_ico(file_name, "logo3.ico", icon_sizes=[(16, 16), (32, 32)])
