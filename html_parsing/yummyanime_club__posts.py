#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag


def get_text(el: Tag) -> str:
    text = el.get_text(strip=True)
    return text.replace("\xa0", " ")


def parse_post_block(post_block: Tag) -> None:
    title_el = post_block.select_one(".post-title")
    url_post = urljoin(URL, title_el["href"])
    title = get_text(title_el)
    category = get_text(post_block.select_one(".post-title-category"))

    post_time = get_text(post_block.select_one(".post-time"))
    p_text, p_author, p_comments = post_block.select("p")
    post_text = get_text(p_text)
    author = get_text(p_author.a)
    comments = get_text(p_comments)

    print(title, category, url_post, sep=" | ")
    print(post_time, author, comments, sep=" | ")
    print(repr(post_text))
    print("\n" + "-" * 100 + "\n")


URL = "https://yummyanime.club/posts"

headers = {
    "Host": "yummyanime.club",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0",
}

session = requests.session()
session.headers.update(headers)

rs = session.get(URL)
root = BeautifulSoup(rs.content, "html.parser")

for post_block in root.select(".post-block"):
    parse_post_block(post_block)

"""
Студия «Ghibli» | статья | https://yummyanime.club/post/466
20 Июн 2020 | Nomia | Комментариев: 34
'Название «Ghibli» студии дал основатель - Хаяо Миядзаки. На выбор повлиял его интерес к авиации, в частности самолёт «Caproni Ca.309 Ghibli» итальянского производства. Слово «Ghibli» ливийского происхождения, и означает ветер Сирокко, дующий с юго-востока...'

----------------------------------------------------------------------------------------------------

История студии. Manglobe. "От рассвета до заката" часть 2 | статья | https://yummyanime.club/post/465
6 Июн 2020 | DreamEvil | Комментариев: 20
'Акт VIII. Начало конца«Страна чудес» со своей жестокостью и визуалом великолепно показала себя как в Америке, так и в Европе. А вот на родине сериал не удостоился даже тысячного тиража на DVD. Ожидаемый исход для студии, которая так и не смогла определить свою целевую аудиторию. Не помогли даже лест ...'

----------------------------------------------------------------------------------------------------

История студии. Manglobe. "От рассвета до заката" часть 1 | статья | https://yummyanime.club/post/464
6 Июн 2020 | DreamEvil | Комментариев: 13
'История студии. Manglobe ПредисловиеИтак, год, проведенный в творческой изоляции, также именуемой вооруженными силами, не прошел даром. Подобное заныривание в пучину сюрреализма и тупости подтолкнуло к новому творческому порыву. В этот раз мы поговорим, к сожалению, не очень подробно (ввиду отс ...'

...

"""
