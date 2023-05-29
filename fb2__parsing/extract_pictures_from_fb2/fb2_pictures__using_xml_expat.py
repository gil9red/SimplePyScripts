#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""Скрипт парсит файл формата fb2, вытаскивает из него картинки и сохраняет их в папке с таким же названием,
как файл fb2."""


import base64
import io
import os
import traceback
import xml.parsers.expat

# pip install humanize
from humanize import naturalsize as sizeof_fmt

from PIL import Image

from common import get_file_name_from_binary


def do(file_name, output_dir="output", debug=True):
    dir_fb2 = os.path.basename(file_name)
    dir_im = os.path.join(output_dir, dir_fb2)
    os.makedirs(dir_im, exist_ok=True)
    debug and print(dir_im + ":")

    PARSE_DATA = {
        "last_start_tag": None,
        "last_tag_attrs": None,
        "last_tag_data": "",
        "total_image_size": 0,
        "number": 1,
    }

    def on_start_element(name, attrs):
        PARSE_DATA["last_start_tag"] = name
        PARSE_DATA["last_tag_attrs"] = attrs
        PARSE_DATA["last_tag_data"] = ""

    def on_char_data(data):
        if PARSE_DATA["last_start_tag"] != "binary":
            return

        PARSE_DATA["last_tag_data"] += data

    def on_end_element(name):
        if name != "binary":
            return

        data = PARSE_DATA["last_tag_data"]

        try:
            im_id = PARSE_DATA["last_tag_attrs"]["id"]
            content_type = PARSE_DATA["last_tag_attrs"]["content-type"]

            im_file_name = get_file_name_from_binary(im_id, content_type)
            im_file_name = os.path.join(dir_im, im_file_name)

            im_data = base64.b64decode(data.encode())

            count_bytes = len(im_data)
            PARSE_DATA["total_image_size"] += count_bytes

            with open(im_file_name, mode="wb") as f:
                f.write(im_data)

            im = Image.open(io.BytesIO(im_data))
            debug and print(
                "    {}. {} {} format={} size={}".format(
                    PARSE_DATA["number"],
                    im_id,
                    sizeof_fmt(count_bytes),
                    im.format,
                    im.size,
                )
            )

            PARSE_DATA["number"] += 1

        except:
            traceback.print_exc()

    p = xml.parsers.expat.ParserCreate()
    p.StartElementHandler = on_start_element
    p.CharacterDataHandler = on_char_data
    p.EndElementHandler = on_end_element

    with open(file_name, "rb") as fb2:
        p.Parse(fb2.read(), 1)

    file_size = os.path.getsize(file_name)
    debug and print()
    debug and print("fb2 file size =", sizeof_fmt(file_size))
    debug and print(
        "total image size = {} ({:.2f}%)".format(
            sizeof_fmt(PARSE_DATA["total_image_size"]),
            PARSE_DATA["total_image_size"] / file_size * 100,
        )
    )


if __name__ == "__main__":
    fb2_file_name = "../input/Непутевый ученик в школе магии 1. Зачисление в школу (Часть 1).fb2"
    do(fb2_file_name)
