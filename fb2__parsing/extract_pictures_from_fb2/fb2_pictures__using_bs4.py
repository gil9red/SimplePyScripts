#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""Скрипт парсит файл формата fb2, вытаскивает из него картинки и сохраняет их в папке с таким же названием,
как файл fb2."""


import os
import base64
import io
import traceback

from bs4 import BeautifulSoup
from PIL import Image

import sys
sys.path.append("..")

from common import sizeof_fmt, get_file_name_from_binary


def do(file_name, output_dir="output", debug=True):
    dir_fb2 = os.path.basename(file_name)
    dir_im = os.path.join(output_dir, dir_fb2)
    os.makedirs(dir_im, exist_ok=True)
    debug and print(dir_im + ":")

    total_image_size = 0

    with open(file_name, "rb") as fb2:
        root = BeautifulSoup(fb2, "html.parser")

        binaries = root.select("binary")
        for i, binary in enumerate(binaries, 1):
            try:
                im_id = binary.attrs["id"]
                content_type = binary.attrs["content-type"]

                im_file_name = get_file_name_from_binary(im_id, content_type)
                im_file_name = os.path.join(dir_im, im_file_name)

                im_data = base64.b64decode(binary.text.encode())

                count_bytes = len(im_data)
                total_image_size += count_bytes

                with open(im_file_name, mode="wb") as f:
                    f.write(im_data)

                im = Image.open(io.BytesIO(im_data))
                debug and print(
                    "    {}. {} {} format={} size={}".format(
                        i, im_id, sizeof_fmt(count_bytes), im.format, im.size
                    )
                )

            except:
                traceback.print_exc()

    file_size = os.path.getsize(file_name)
    debug and print()
    debug and print("fb2 file size =", sizeof_fmt(file_size))
    debug and print(
        "total image size = {} ({:.2f}%)".format(
            sizeof_fmt(total_image_size), total_image_size / file_size * 100
        )
    )


if __name__ == "__main__":
    fb2_file_name = "../input/Непутевый ученик в школе магии 1. Зачисление в школу (Часть 1).fb2"
    do(fb2_file_name)
