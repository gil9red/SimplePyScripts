#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# TODO: парсинг страницы торрент, вытаскивание характеристик, описания, скриншотов, торрент-файла и магнет-ссылки

from bs4 import BeautifulSoup


root = BeautifulSoup(open("1.htm", "rb"), "lxml")

details = root.select_one("#details")
print(details.text.strip())
