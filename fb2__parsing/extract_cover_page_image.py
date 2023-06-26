#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import base64
from bs4 import BeautifulSoup
from common import get_attribute_value_by_local_name


def get_cover_page_image(root) -> (bytes, str):
    cover_page_image = root.select_one("coverpage > image")

    # Вытаскиваем значение атрибута href
    id_image = get_attribute_value_by_local_name(cover_page_image, "href")

    # "#cover.jpg" -> "cover.jpg"
    id_image = id_image[1:]

    # Получится, например, такой css-селектор: "[id='cover.jpg']"
    binary = root.select_one(f"[id='{id_image}']")

    # image/jpeg -> jpeg
    content_type = binary.attrs["content-type"].split("/")[-1]

    # Содержимое тега будет извлечено и представлено в виде байтов
    data = binary.text.encode("utf-8")

    return base64.b64decode(data), {"jpeg": "jpg", "png": "png"}[content_type]


if __name__ == "__main__":
    import glob
    import os

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    for fb2_file_name in glob.glob("input/*.fb2"):
        with open(fb2_file_name, encoding="utf-8") as f:
            root = BeautifulSoup(f, "html.parser")

        img_data, fmt = get_cover_page_image(root)

        file_name = os.path.basename(fb2_file_name) + "." + fmt
        file_name = os.path.join(output_dir, file_name)

        with open(file_name, "wb") as f:
            f.write(img_data)
