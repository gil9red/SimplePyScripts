#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""Скрипт для скачивания примеров как проекты: сохранение в папки, в файлы"""


from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def get_path_and_content(url: str) -> tuple[str, str]:
    rs = requests.get(url)
    root = BeautifulSoup(rs.content, "lxml")

    path = root.select_one(".subtitle").text.strip()
    content = root.select_one(".descr").text.strip()
    return path, content


def get_content(url: str) -> str:
    _, content = get_path_and_content(url)
    return content


def get_list_urls_files(url: str) -> list[tuple[str, str]]:
    rs = requests.get(url)
    root = BeautifulSoup(rs.content, "lxml")

    urls_files_list = []

    for p in root.select("p"):
        if p.text.strip() != "Files:":
            continue

        ul = p.find_next_sibling("ul")
        for a in ul.select("li > a"):
            abs_url = urljoin(url, a["href"])
            file_name = a.text.strip()

            urls_files_list.append((abs_url, file_name))

    return urls_files_list


if __name__ == "__main__":
    import os

    url = "http://doc.qt.io/qt-5/qtwebengine-webenginewidgets-simplebrowser-simplebrowser-pro.html"
    path, content = get_path_and_content(url)
    print(path, content.encode("utf-8"))

    content = get_content(url)
    print(content.encode("utf-8"))

    print()
    url = "http://doc.qt.io/qt-5/qtwebengine-webenginewidgets-simplebrowser-example.html"
    urls_files_list = get_list_urls_files(url)
    print(f"Files: {len(urls_files_list)}")

    for i, (url, path) in enumerate(urls_files_list, 1):
        print(f'{i}. "{path}": {url}')

        dirs = os.path.dirname(path)
        os.makedirs(dirs, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            content = get_content(url)
            f.write(content)
