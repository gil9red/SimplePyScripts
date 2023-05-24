#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from bs4 import BeautifulSoup


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0",
}

rs = requests.get("https://www.techcult.ru/technology", headers=headers)
root = BeautifulSoup(rs.content, "html.parser")

for a in root.select("a.pad"):
    url = a["href"]
    title = a.h2.get_text(strip=True)
    print(title, url)

# Фильтр из аэрогеля бесплатно и быстро очистит любые объемы воды https://www.techcult.ru/technology/8196-filtr-iz-aerogelya-bystro-ochishaet-lyubye-obemy-vody
# Система тросиков Wireality сделает виртуальные предметы реальными и осязаемыми https://www.techcult.ru/technology/8199-tehnologiya-wireality-delaet-virtualnye-predmety-realnymi
# Графен превосходно справился с защитой труб от бактериальной коррозии https://www.techcult.ru/technology/8193-grafen-zashishaet-truby-ot-bakterialnoj-korrozii
# Алмазные нанонити запасают энергию в три раза эффективнее Li-Ion батарей https://www.techcult.ru/technology/8194-nanoniti-zapasayut-energiyu-effektivnee-litij-ionnyh-batarej
# Искусственный интеллект Fujitsu справляется с управлением Токийским портом лучше людей https://www.techcult.ru/technology/8190-ii-spravlyaetsya-s-upravleniem-tokijskim-portom-luchshe-lyudej
# ...
