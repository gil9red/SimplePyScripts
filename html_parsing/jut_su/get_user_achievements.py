#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
import time

from dataclasses import dataclass
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from common import session


@dataclass
class Achievement:
    icon_url: str
    title: str
    description: str
    date_str: str
    video_url: str


def get_achievements(
    url: str,
    start_page: int = 1,
    need_total_items: int = None,
    reversed: bool = False,
) -> list[Achievement]:
    data = {
        "ajax_load": "yes",
        "start_from_page": start_page,
    }

    items = []

    while True:
        rs = session.post(url, data=data)
        rs.raise_for_status()

        root = BeautifulSoup(rs.text, "html.parser")

        achiv_items = root.select(".achiv_all_in")
        if not achiv_items:
            break

        for item in achiv_items:
            icon_url = None
            icon_style = item.select_one(".achiv_all_icon")["style"]
            match = re.search(r"url\(.(.+).\)", icon_style)
            if not match:
                print("[-] Not found icon!")
            else:
                icon_url = match.group(1)

            title = item.select_one(".achiv_all_text_title").get_text(strip=True)
            description = item.select_one(".achiv_all_text_description").get_text(
                strip=True
            )

            tag_date_a = item.select_one(".achiv_all_text_date > a")
            date_str = tag_date_a.get_text(strip=True)
            video_url = urljoin(rs.url, tag_date_a["href"])

            items.append(Achievement(icon_url, title, description, date_str, video_url))

        if need_total_items and len(items) >= need_total_items:
            items = items[:need_total_items]
            break

        data["start_from_page"] += 1

        time.sleep(1)

    if reversed:
        items.reverse()

    return items


if __name__ == "__main__":
    url = "https://jut.su/user/gil9red/achievements/"
    items = get_achievements(url)

    print(f"Achievements ({len(items)}):")
    for item in items:
        print(f"    {item}")

    """
    Achievements (2690):
        Achievement(icon_url='https://gen.jut.su/uploads/achievements/icons/5699.jpg', title='Сильнее, чем он', description='Нойтора против Ичиго', date_str='сегодня в 14:07', video_url='https://jut.su/bleach/episode-190.html')
        Achievement(icon_url='https://gen.jut.su/uploads/achievements/icons/5698.jpg', title='Velonica', description='Посмотрите 9 опенинг', date_str='сегодня в 13:54', video_url='https://jut.su/bleach/episode-190.html')
        Achievement(icon_url='https://gen.jut.su/uploads/achievements/icons/5664.jpg', title='Chu-Bura', description='Посмотрите 8 опенинг', date_str='сегодня в 13:27', video_url='https://jut.su/bleach/episode-168.html')
        ...
        Achievement(icon_url='https://gen.jut.su/uploads/achievements/icons/1607.jpg', title='Сага начинается', description='Джонатан встречает Дио', date_str='2 ноября 2019', video_url='https://jut.su/jojo-bizarre-adventure/season-1/episode-1.html')
        Achievement(icon_url='https://gen.jut.su/uploads/achievements/icons/1606.jpg', title='Юноша из низов', description='Вы познакомились с Дио', date_str='2 ноября 2019', video_url='https://jut.su/jojo-bizarre-adventure/season-1/episode-1.html')
        Achievement(icon_url='https://gen.jut.su/uploads/achievements/icons/1605.jpg', title='Благородный ДжоДжо', description='Вы познакомились с Джонатаном', date_str='2 ноября 2019', video_url='https://jut.su/jojo-bizarre-adventure/season-1/episode-1.html')
    """
