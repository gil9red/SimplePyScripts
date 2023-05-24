#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from urllib.parse import quote

import requests
from bs4 import BeautifulSoup


def get_alban(text: str) -> str:
    headers = {
        "Host": "javer.kiev.ua",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0",
    }

    params = f"?input={quote(text, encoding='cp1251')}&s={quote('Пиривеcти', encoding='cp1251')}"
    rs = requests.get("http://javer.kiev.ua/alban.php" + params, headers=headers)

    root = BeautifulSoup(rs.text, "html.parser")
    return root.select_one("textarea:nth-of-type(2)").get_text(strip=True)


if __name__ == "__main__":
    text = get_alban("привет")
    print(text)
    assert text == "превед"

    print()

    text = """
Я памятник себе воздвиг нерукотворный,
К нему не зарастет народная тропа,
Вознесся выше он главою непокорной
Александрийского столпа.
    """.strip()
    text = get_alban(text)
    print(text)
    assert (
        text
        == """
Я памятнег себе воздвиг нирукотворный,
К ниму ни зарастед народнайа тропа,
Вознессо выше ан главайу нипакорной
Александрийсково столпа.
    """.strip()
    )
