#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import base64
import io

# pip install pillow
from PIL import Image


def img_to_base64_html(file_name__or__bytes__or__file_object: str | bytes | io.IOBase) -> str:
    arg = file_name__or__bytes__or__file_object

    if isinstance(arg, str):
        with open(arg, mode="rb") as f:
            img_bytes = f.read()

    elif isinstance(arg, bytes):
        img_bytes = arg

    else:
        img_bytes = arg.read()

    bytes_io = io.BytesIO(img_bytes)
    img = Image.open(bytes_io)

    img_base64 = base64.b64encode(img_bytes).decode("utf-8")
    return f"data:image/{img.format.lower()};base64,{img_base64}"


if __name__ == "__main__":
    file_name = "img.jpg"
    img_base64 = img_to_base64_html(file_name)
    print(f"[len {len(img_base64)}]: {img_base64[:50]}...")

    with open(file_name + "_base64.txt", mode="w", encoding="utf-8") as f:
        f.write(img_base64)
