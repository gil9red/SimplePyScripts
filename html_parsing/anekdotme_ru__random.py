#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from bs4 import BeautifulSoup


def get_anekdot() -> str:
    rs = requests.get("http://anekdotme.ru/random")
    root = BeautifulSoup(rs.content, "html.parser")

    el = root.select_one(".anekdot_text")
    return el.get_text(strip=True, separator="\n")


if __name__ == "__main__":
    print(get_anekdot())
    """
    Урок языковедения в школе. Училка распинается:
    — Есть языки, в которых двойное отрицание означает отрицание, утверждение
    и отрицание все-равно означает отрицание. Но нет ни одного языка, где
    бы двойное утверждение означало отрицание!
    Голос с последней парты:
    — Ну да, конечно!
    """
