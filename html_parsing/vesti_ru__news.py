#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


rs = requests.get("https://www.vesti.ru/news")
root = BeautifulSoup(rs.content, "html.parser")

for i in root.select(".b-item__info"):
    title = i.select_one(".b-item__title")
    text = title.a.get_text(strip=True)
    url = urljoin(rs.url, title.a["href"])
    print(text, url)

# "Спасибо за освобождение, но...": европолитиков понесло https://www.vesti.ru/doc.html?id=3263997
# Инсайдеры назвали дату старта сезона "Формулы-1" https://www.vesti.ru/doc.html?id=3264031
# Кошмарная цифра: шведский подход против коронавируса не сработал https://www.vesti.ru/doc.html?id=3263988
# В Подмосковье электричка сбила двух мужчин, один скончался https://www.vesti.ru/doc.html?id=3264028
# Российские военные оставили Италию выздоравливающей https://www.vesti.ru/doc.html?id=3263979
# Ограничения и образование: ситуация в России https://www.vesti.ru/doc.html?id=3263969
# ...
