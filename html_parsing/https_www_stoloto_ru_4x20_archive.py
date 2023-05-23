#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import csv
from urllib.request import urlopen

from bs4 import BeautifulSoup


def parse_page(page_number: int) -> tuple[str, list[str]]:
    url = f"https://www.stoloto.ru/4x20/archive/{page_number}"
    root = BeautifulSoup(urlopen(url), "html.parser")

    # Название, пример: "Результаты тиража № 1, 31 декабря 2016 в 15:10"
    title = root.select_one("#content > h2").text.strip()

    # Вытаскиваем дату, пример: "31 декабря 2016 в 15:10"
    date_time_str = title.split(", ")[1]

    # Вытаскиваем номера, пример: ['20', '2', '10', '4', '2', '16', '9', '17']
    numbers = [x.text.strip() for x in root.select(".winning_numbers > ul > li")]

    return date_time_str, numbers


max_page_number = 4
result = []

# Перебор страниц от 1 до <max_page_number> включительно
for page_number in range(1, max_page_number + 1):
    date_time_str, numbers = parse_page(page_number)

    # Список чисел преобразуем в строку:
    # ['20', '2', '10', '4', '2', '16', '9', '17'] -> '20 2 10 4 2 16 9 17'
    numbers = " ".join(numbers)
    result.append((page_number, date_time_str, numbers))

print(result)

with open("lotto.csv", "w", encoding="utf-8", newline="") as f:
    file = csv.writer(f)
    file.writerows(result)
