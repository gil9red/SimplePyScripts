#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from bs4 import BeautifulSoup


session = requests.session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0"


def get_lyrics(url: str) -> str:
    rs = session.get(url)
    root = BeautifulSoup(rs.content, "html.parser")

    items = [
        block.get_text(strip=True) for block in root.select(".lyrics__content__ok")
    ]
    return "\n".join(items)


if __name__ == "__main__":
    url = "https://www.musixmatch.com/lyrics/Fun-Mode/Друид"
    print(get_lyrics(url))
    # Против каждого класса есть приемы свои
    # Но порвется шаблон, ведь существуют они
    # Гремучая смесь танка, хила и дд
    # На арене встречаешь - и пукан твой в огне
    #
    # ...
    #
    # Загляни в арены топ - там увидишь ты меня
    # Где затмение кастует волосатая херня
    # В мишке танчит, корни жмут, смену формы не поймут
    # Мы его почти убили, но полено затащило
