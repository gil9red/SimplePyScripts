#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag


def get_text(el: Tag) -> str:
    text = el.get_text(strip=True)
    return text.replace("\xa0", " ")


def parse_update_anime(update_el: Tag):
    title = get_text(update_el.select_one(".update-title"))
    update_date = get_text(update_el.select_one(".update-date"))
    update_info = get_text(update_el.select_one(".update-info"))
    url_anime = urljoin(URL, update_el["href"])
    url_img = urljoin(URL, update_el.select_one(".update-img")["src"])

    print(f"{update_date} | {title} - {update_info}")
    print(f"    {url_anime} | {url_img}\n")


URL = "https://yummyanime.club/anime-updates"

headers = {
    "Host": "yummyanime.club",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0",
}

session = requests.session()
session.headers.update(headers)

rs = session.get(URL)
root = BeautifulSoup(rs.content, "html.parser")

for update_anime in root.select(".update-list > li > a"):
    parse_update_anime(update_anime)

"""
8 Авг | Олимпия Киклос - Добавлены 10-я и 11-я серии: Озвучка AniDUB. Плеер Kodik
    https://yummyanime.club/catalog/item/olimpiya-kiklos | https://yummyanime.club/img/posters/1588708142.jpg

8 Авг | Дека-данс - Добавлена 5-я серия: Озвучка AniLibria. Плеер Kodik
    https://yummyanime.club/catalog/item/deka-dans | https://yummyanime.club/img/posters/1590605545.jpg

8 Авг | Лазурные огни - Добавлена 6-я серия: Озвучка StudioBand. Плеер Kodik
    https://yummyanime.club/catalog/item/lazurnye-ogni | https://yummyanime.club/img/posters/1593622315.jpg

8 Авг | Как и ожидал, моя школьная романтическая жизнь не удалась [ТВ-1] - Добавлена 6-я серия: Озвучка AniLibria. Плеер Kodik
    https://yummyanime.club/catalog/item/rozovaya-pora-moej-shkolnoj-zhizni-sploshnoj-obman | https://yummyanime.club/img/posters/1574695886.jpg

...

"""
