#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""Скрипт для скачивания главы по указанному url."""


import ast
import re
import zipfile

import requests


PATTERN = re.compile(r"\.init\(.*(\[\[.+\]\]).*\)")


def get_url_images(url):
    print("Start get_url_images with url:", url)

    rs = requests.get(url)

    match = PATTERN.search(rs.text)
    if not match:
        raise Exception(
            "Не получилось из страницы вытащить список картинок главы. "
            "Используемое регулярное выражение: ",
            PATTERN.pattern,
        )

    match = match.group(1)
    print("Match:", match)

    urls = ast.literal_eval(match)
    print("After parse match:", urls)

    return [i[0] + i[2] for i in urls]


def save_urls_to_zip(zip_file_name, urls) -> None:
    if not urls:
        print("Cписок изображений пустой.")
        return

    # Создаем архив, у которого именем будет номер главы
    with zipfile.ZipFile(
        zip_file_name, mode="w", compression=zipfile.ZIP_DEFLATED
    ) as f:
        import os
        from urllib.request import urlretrieve

        for img_url in urls:
            # Вытаскиваем имя файла
            file_name = os.path.basename(img_url)

            # Имя файла будет {номер_главы}_{номер_страницы}.png
            print(img_url, file_name)

            # Скачиваем файл
            urlretrieve(img_url, file_name)

            # Помещаем в архив
            f.write(file_name)

            # Удаляем файл
            os.remove(file_name)


if __name__ == "__main__":
    import traceback
    from pathlib import Path

    url = "https://readmanga.live/one_punch_man__A1bc88e/vol1/1"

    try:
        urls = get_url_images(url)
        print(f"Urls ({len(urls)}):")
        for i, x in enumerate(urls, 1):
            print(f"{i}. {x}")

        url_file_name = (
            url.replace("http://", "").replace("https://", "").replace("/", "_")
        )
        file_name = Path(__file__).resolve().name + " - " + url_file_name + ".zip"
        save_urls_to_zip(file_name, urls)
        print("Save to filename:", file_name)

    except Exception as e:
        print(f"Error: {e}\n\n{traceback.format_exc()}")
