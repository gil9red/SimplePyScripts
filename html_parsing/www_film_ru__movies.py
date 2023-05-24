#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


URL = "https://www.film.ru/movies"
rs = requests.get(URL)
root = BeautifulSoup(rs.content, "html.parser")

for a in root.select("div.rating.infinite_scroll > a"):
    title = a.strong.get_text(strip=True)
    url = urljoin(rs.url, a["href"])
    print(title, url)

# Проклятый путь https://www.film.ru/articles/semeynaya-drama-s-tommi-ganom-v-ruke
# Унесенные призраками https://www.film.ru/articles/klassika-anime-unesennye-prizrakami
# Адаптация https://www.film.ru/articles/lukavoe-naglyadnoe-posobie-po-ekranizacii
# ...
# Первый мститель: Другая война https://www.film.ru/articles/so-schitom-ili-na-schite
