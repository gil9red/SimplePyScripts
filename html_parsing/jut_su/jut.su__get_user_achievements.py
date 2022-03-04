#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import re
from urllib.parse import urljoin
from typing import List, NamedTuple
import time

from bs4 import BeautifulSoup
import requests


class Achievement(NamedTuple):
    icon_url: str
    title: str
    description: str
    date_str: str
    video_url: str


def get_achievements(url: str, reversed=False) -> List[Achievement]:
    data = {
        "ajax_load": "yes",
        "start_from_page": 1,
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
    }

    items = []

    while True:
        rs = requests.post(url, data=data, headers=headers)
        rs.raise_for_status()

        root = BeautifulSoup(rs.content, 'html.parser')

        achiv_items = root.select('.achiv_all_in')
        if not achiv_items:
            break

        for item in achiv_items:
            icon_url = None
            icon_style = item.select_one('.achiv_all_icon')['style']
            match = re.search(r"url\(.(.+).\)", icon_style)
            if not match:
                print('[-] Not found icon!')
            else:
                icon_url = match.group(1)

            title = item.select_one('.achiv_all_text_title').get_text(strip=True)
            description = item.select_one('.achiv_all_text_description').get_text(strip=True)

            tag_date_a = item.select_one('.achiv_all_text_date > a')
            date_str = tag_date_a.get_text(strip=True)
            video_url = urljoin(rs.url, tag_date_a['href'])

            items.append(
                Achievement(icon_url, title, description, date_str, video_url)
            )

        data["start_from_page"] += 1

        time.sleep(1)

    if reversed:
        items.reverse()

    return items


if __name__ == '__main__':
    url = 'https://jut.su/user/gil9red/achievements/'
    items = get_achievements(url)

    print(f'Achievements ({len(items)}):')
    for item in items:
        print(f'    {item}')

    # Achievements (102):
    #     Achievement(icon_url='https://jut.su/uploads/achievements/icons/1706.jpg', title='Шпага и пистолет', description='Хол Хорс атакует Польнареффа', date_str='сегодня в 01:48', video_url='https://jut.su/jojo-bizarre-adventure/season-2/episode-10.html')
    #     Achievement(icon_url='https://jut.su/uploads/achievements/icons/1705.jpg', title='Мачо-ковбой', description='Вы познакомились с Хол Хорсом', date_str='сегодня в 01:42', video_url='https://jut.su/jojo-bizarre-adventure/season-2/episode-10.html')
    #     Achievement(icon_url='https://jut.su/uploads/achievements/icons/1704.jpg', title='Местные нравы', description='Польнарефф и туалеты', date_str='сегодня в 01:34', video_url='https://jut.su/jojo-bizarre-adventure/season-2/episode-10.html')
    #     Achievement(icon_url='https://jut.su/uploads/achievements/icons/1703.jpg', title='Любитель вишенок', description='Не пугайся, Джотаро', date_str='сегодня в 01:27', video_url='https://jut.su/jojo-bizarre-adventure/season-2/episode-9.html')
    #     Achievement(icon_url='https://jut.su/uploads/achievements/icons/1702.jpg', title='Вишенка на торте', description='Rerorerorerorero', date_str='сегодня в 01:11', video_url='https://jut.su/jojo-bizarre-adventure/season-2/episode-9.html')
    # ...
    #     Achievement(icon_url='https://jut.su/uploads/achievements/icons/1610.jpg', title='Sono Chi no Sadame', description='Посмотрите 1 опенинг', date_str='2 ноября', video_url='https://jut.su/jojo-bizarre-adventure/season-1/episode-2.html')
    #     Achievement(icon_url='https://jut.su/uploads/achievements/icons/1609.jpg', title='Загадочный артефакт', description='Что скрывает маска?', date_str='2 ноября', video_url='https://jut.su/jojo-bizarre-adventure/season-1/episode-1.html')
    #     Achievement(icon_url='https://jut.su/uploads/achievements/icons/1608.jpg', title='Это был я, Дио!', description='Гость Джостаров творит бесчинства', date_str='2 ноября', video_url='https://jut.su/jojo-bizarre-adventure/season-1/episode-1.html')
    #     Achievement(icon_url='https://jut.su/uploads/achievements/icons/1607.jpg', title='Сага начинается', description='Джонатан встречает Дио', date_str='2 ноября', video_url='https://jut.su/jojo-bizarre-adventure/season-1/episode-1.html')
    #     Achievement(icon_url='https://jut.su/uploads/achievements/icons/1606.jpg', title='Юноша из низов', description='Вы познакомились с Дио', date_str='2 ноября', video_url='https://jut.su/jojo-bizarre-adventure/season-1/episode-1.html')
    #     Achievement(icon_url='https://jut.su/uploads/achievements/icons/1605.jpg', title='Благородный ДжоДжо', description='Вы познакомились с Джонатаном', date_str='2 ноября', video_url='https://jut.su/jojo-bizarre-adventure/season-1/episode-1.html')
