#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""Скрипт парсит файл формата fb2, вытаскивает из него картинки и сохраняет их в папке с таким же названием,
как файл fb2.
Аналогичен fb2_pictures.py, только для парсинга используются регулярные выражения, а не разбор
через xml парсер. Причиной создания этого аналога в том, что если парсер не сможет распарсить fb2, например,
при поломанной структуре fb2, тогда скрипт не сможет вытащить картинки."""


import base64
import io
import os
import re
import traceback

# pip install humanize
from humanize import naturalsize as sizeof_fmt

from PIL import Image

from common import get_file_name_from_binary


def do(file_name, output_dir="output", debug=True):
    dir_fb2 = os.path.basename(file_name)
    dir_im = os.path.join(output_dir, dir_fb2)
    os.makedirs(dir_im, exist_ok=True)
    debug and print(dir_im + ":")

    total_image_size = 0

    with open(file_name, encoding="utf-8") as fb2:
        pattern = re.compile(
            '<binary ((content-type=".+?") (id=".+?")'
            '|(id=".+?") (content-type=".+?")) *?>(.+?)</binary>',
            re.DOTALL,
        )

        find_content_type = re.compile('content-type="(.+?)"')
        find_id = re.compile('id="(.+?)"')

        for i, binary in enumerate(pattern.findall(fb2.read()), 1):
            try:
                im_id, content_type, im_base64 = None, None, None

                for part in binary:
                    if not part:
                        continue

                    match_id = find_id.search(part)
                    if im_id is None and match_id is not None:
                        im_id = match_id.group(1)

                    match_content_type = find_content_type.search(part)
                    if content_type is None and match_content_type is not None:
                        content_type = match_content_type.group(1)

                    if match_id is None and match_content_type is None:
                        im_base64 = part

                im_file_name = get_file_name_from_binary(im_id, content_type)
                im_file_name = os.path.join(dir_im, im_file_name)

                im_data = base64.b64decode(im_base64.encode())

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
