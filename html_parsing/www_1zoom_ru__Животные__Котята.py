#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from bs4 import BeautifulSoup


def get_imgs(page: int) -> list:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    }
    url = f"https://www.1zoom.ru/Животные/Котята/t2/{page}"

    rs = requests.get(url, headers=headers)
    root = BeautifulSoup(rs.content, "html.parser")

    return [img["src"] for img in root.select("#suda .ph > a > img[src]")]


if __name__ == "__main__":
    # Парсинг первой страницы
    imgs = get_imgs(1)
    print(len(imgs), imgs)
    # 30 ['https://s1.1zoom.ru/prev2/581/Ginger_color_Cute_Kittens_580356_300x214.jpg', ...

    # Парсинг второй страницы
    imgs = get_imgs(2)
    print(len(imgs), imgs)
    # 30 ['https://s1.1zoom.ru/prev2/570/Cats_White_background_Kittens_569316_300x200.jpg', ...
