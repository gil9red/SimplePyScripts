#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт парсит файл формата fb2, вытаскивает из него картинки и сохраняет их в папке с таким же названием, как файл fb2.
"""


import base64
import io
import os
import traceback

from typing import Iterator

# pip install humanize
from humanize import naturalsize as sizeof_fmt

from PIL import Image

from common import get_file_name_from_binary


def find_inner(text: str, start_str: str, end_str: str) -> tuple[str | None, int]:
    idx_start = text.find(start_str)
    if idx_start == -1:
        return None, -1

    idx_end = text.find(end_str, idx_start + len(start_str))
    if idx_end == -1:
        return None, -1

    return (
        text[idx_start + len(start_str) : idx_end],
        idx_end + len(end_str)
    )


def iter_blocks(text: str, start_str: str, end_str: str) -> Iterator[str]:
    block, idx_next_start = find_inner(text, start_str, end_str)
    if not block:
        return
    yield block

    while block:
        text = text[idx_next_start:]
        block, idx_next_start = find_inner(text, start_str, end_str)
        if not block:
            break

        yield block


def do(file_name, output_dir="output", debug=True) -> None:
    dir_fb2 = os.path.basename(file_name)
    dir_im = os.path.join(output_dir, dir_fb2)
    os.makedirs(dir_im, exist_ok=True)
    debug and print(dir_im + ":")

    total_image_size = 0

    with open(file_name, encoding="utf-8") as fb2:
        for i, binary in enumerate(
            iter_blocks(fb2.read(), "<binary ", "</binary>"),
            start=1,
        ):
            try:
                binary_header, idx_next_start = find_inner(binary, "", ">")

                im_id, _ = find_inner(binary_header, 'id="', '"')
                content_type, _ = find_inner(binary_header, 'content-type="', '"')

                im_base64 = binary[idx_next_start:]

                im_file_name = get_file_name_from_binary(im_id, content_type)
                im_file_name = os.path.join(dir_im, im_file_name)

                im_data = base64.b64decode(im_base64.encode())

                count_bytes = len(im_data)
                total_image_size += count_bytes

                with open(im_file_name, mode="wb") as f:
                    f.write(im_data)

                im = Image.open(io.BytesIO(im_data))
                debug and print(
                    f"    {i}. {im_id} {sizeof_fmt(count_bytes)} format={im.format} size={im.size}"
                )
            except:
                traceback.print_exc()

        file_size = os.path.getsize(file_name)
        debug and print()
        debug and print("fb2 file size =", sizeof_fmt(file_size))
        debug and print(
            f"total image size = {sizeof_fmt(total_image_size)} ({total_image_size / file_size * 100:.2f}%)"
        )


if __name__ == "__main__":
    fb2_file_name = "../input/Непутевый ученик в школе магии 1. Зачисление в школу (Часть 1).fb2"
    do(fb2_file_name)
