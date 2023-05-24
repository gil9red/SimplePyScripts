#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys

import requests
from bs4 import BeautifulSoup

# For import ascii_table__simple_pretty__ljust.py
sys.path.append("..")
from ascii_table__simple_pretty__ljust import print_pretty_table


url = "https://ru.wikipedia.org/wiki/Список_персонажей_Tekken"
rs = requests.get(url)
root = BeautifulSoup(rs.content, "html.parser")

number = 0
items = []

for tr in root.select_one(".wikitable").select("tbody > tr"):
    td_list = tr.select("td")
    if len(td_list) < 3:
        continue

    for sub in tr.select("sup"):
        sub.decompose()

    number += 1
    person_td, _, *games_td = td_list

    name = person_td.get_text(strip=True)
    was_presents = [td.img["title"] == "Да" for td in games_td]
    if sum(was_presents) != 1:
        continue

    num = was_presents.index(True) + 1
    game = "Tekken " + ("" if num == 1 else str(num))
    items.append((name, game))


print(f"Total: {number}, unique: {len(items)}\n")
# Total: 87, unique: 39

print_pretty_table([("PERSON", "GAME")] + items)
# PERSON              | GAME
# --------------------+---------
# Азазель             | Tekken 6
# Акума               | Tekken 7
# Алекс               | Tekken 2
# Ангел               | Tekken 2
# Ворон               | Tekken 3
# Ган Джек            | Tekken 3
# Гигас               | Tekken 7
# Гис Ховард          | Tekken 7
# Гон                 | Tekken 3
# Джек                | Tekken
# Джек-2              | Tekken 2
# Джек-4              | Tekken 4
# Джек-5              | Tekken 5
# Джек-6              | Tekken 6
# Джек-7              | Tekken 7
# Джози Рисаль        | Tekken 7
# Дзимпати Мисима     | Tekken 5
# Дзюн Кадзама        | Tekken 2
# Доктор Босконович   | Tekken 3
# Дьявол Кадзуми      | Tekken 7
# Истинный Огр        | Tekken 3
# Кадзуми Мисима      | Tekken 7
# Катарина Алвис      | Tekken 7
# Клаудио Серафино    | Tekken 7
# Комбот              | Tekken 4
# Лаки Хлоя           | Tekken 7
# Лерой Смит          | Tekken 7
# Мастер Рэйвен       | Tekken 7
# Михару Хирано       | Tekken 4
# Nancy-MI847J        | Tekken 6
# Ниган               | Tekken 7
# Ноктис Люцис Каэлум | Tekken 7
# Огр                 | Tekken 3
# Роджер              | Tekken 2
# Тайгер Джексон      | Tekken 3
# Фахумрам            | Tekken 7
# Форест Ло           | Tekken 3
# Шахин               | Tekken 7
# Элиза               | Tekken 7
