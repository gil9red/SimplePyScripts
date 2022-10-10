#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import logging
import re

from base64 import b64decode
from dataclasses import dataclass
from typing import Union

from seconds_to_str import seconds_to_str

from common import session


DEBUG = False

logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format='[%(asctime)s] %(levelname)-8s %(message)s',
)

RE_BASE64 = re.compile(r'eval\( *Base64.decode\( *"(.+?)" *\) *\);')
RE_SOME_ACHIV_STR = re.compile(r'some_achiv_str *= *"(.+?)";')
RE_BRACE_CONTENT = re.compile(r'\{(.+?)\}', flags=re.DOTALL)


@dataclass
class Achievement:
    category: str
    title: str
    description: str
    time_start: int
    time_start_pretty: str
    id: int
    hash: str
    icon: str


def parse_raw_anime_achievement(anime_achievement: str) -> dict[str, Union[str, int]]:
    # Пример значения
    """
    category: "events",
    time_start: 704,
    title: "Ядовитый бутон",
    description: "Высвобождение Заэльаппоро",
    icon: js_preres_url + "/uploads/achievements/icons/5703.jpg",
    id: "5703",
    hash: "11560c9068571116"
    """

    values: dict[str, Union[str, int]] = dict()
    for line in anime_achievement.splitlines():
        line = line.strip()
        if not line:
            continue

        key, value = line.split(': ', maxsplit=1)
        key = key.strip()
        value = value.strip().rstrip(',')
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]

        values[key] = value

    values['id'] = int(
        values['id']
    )
    values['time_start'] = int(
        values['time_start']
    )
    values['time_start_pretty'] = seconds_to_str(
        values['time_start']
    )

    return values


def parse_raw_anime_achievements(some_achiv_str: str) -> list[dict[str, Union[str, int]]]:
    # Пример значения:
    """
    var this_anime_achievements = [];
    this_anime_achievements.push({
    category: "events",
    time_start: 704,
    title: "Ядовитый бутон",
    description: "Высвобождение Заэльаппоро",
    icon: js_preres_url + "/uploads/achievements/icons/5703.jpg",
    id: "5703",
    hash: "11560c9068571116"
    });
    this_anime_achievements.push({
    category: "events",
    time_start: 1286,
    title: "Не изменилась",
    description: "Нелл не думает сдаваться",
    icon: js_preres_url + "/uploads/achievements/icons/5704.jpg",
    id: "5704",
    hash: "dc3acd1d8af21525"
    });
    """

    return [
        parse_raw_anime_achievement(value)
        for value in RE_BRACE_CONTENT.findall(some_achiv_str)
    ]


def get_raw_achievements(url: str) -> list[dict[str, str]]:
    logging.debug(f'Загрузка {url}')

    rs = session.get(url)
    rs.raise_for_status()

    text = rs.text

    base64_items = RE_BASE64.findall(text)
    logging.debug(f'Найдено base64: {len(base64_items)}')

    if not base64_items:
        raise Exception(f"Не найдено ни одного base64 по шаблону '{RE_BASE64.pattern}'")

    logging.debug('Поиск some_achiv_str среди base64')

    some_achiv_str: str = ''

    for i, base64_value in enumerate(base64_items, 1):
        logging.debug(f'    {i}. base64: {base64_value}')

        data = b64decode(base64_value)
        logging.debug(f'       data: {data}\n')

        m = RE_SOME_ACHIV_STR.search(data.decode('utf-8'))
        if not m:
            continue

        base64_achiv = m.group(1)
        data = b64decode(base64_achiv)
        some_achiv_str = data.decode('utf-8')
        logging.debug(f'some_achiv_str:\n{some_achiv_str}')

    if not some_achiv_str:
        raise Exception("Не удалось найти some_achiv_str среди base64")

    return parse_raw_anime_achievements(some_achiv_str)


def get_anime_achievement(anime_achievement: dict[str, Union[str, int]]) -> Achievement:
    return Achievement(**anime_achievement)


def get_achievements(url: str) -> list[Achievement]:
    return [
        get_anime_achievement(data)
        for data in get_raw_achievements(url)
    ]


if __name__ == '__main__':
    for url in [
        'https://jut.su/bleeach/episode-1.html',
        'https://jut.su/bleeach/episode-16.html',
        'https://jut.su/bleeach/episode-20.html',
        'https://jut.su/bleeach/episode-21.html',
        'https://jut.su/bleeach/episode-24.html',
        'https://jut.su/bleeach/episode-47.html',
    ]:
        achievements = get_achievements(url)
        print(f'{url} ({len(achievements)}):')

        for achievement in achievements:
            print(f'    {achievement}')

        print()
    """
    https://jut.su/bleeach/episode-1.html (4):
        Achievement(category='credits', title='Asterisk', description='Посмотрите 1 опенинг', time_start=100, time_start_pretty='00:01:40', id=5371, hash='ae60172ce6e31e2e', icon='js_preres_url + "/uploads/achievements/icons/5371.jpg"')
        Achievement(category='heroes', title='Жнец душ', description='Вы познакомились с Рукией', time_start=144, time_start_pretty='00:02:24', id=5372, hash='364b2421c7fe6046', icon='js_preres_url + "/uploads/achievements/icons/5372.jpg"')
        Achievement(category='heroes', title='Заступник', description='Вы познакомились с Ичиго', time_start=223, time_start_pretty='00:03:43', id=5373, hash='e02379c16879ce52', icon='js_preres_url + "/uploads/achievements/icons/5373.jpg"')
        Achievement(category='events', title='Временный шинигами', description='Примеряя роль проводника душ', time_start=1246, time_start_pretty='00:20:46', id=5374, hash='a9af11fc7a5a5fc6', icon='js_preres_url + "/uploads/achievements/icons/5374.jpg"')
    
    https://jut.su/bleeach/episode-16.html (3):
        Achievement(category='heroes', title='Глава Кучики', description='Вы познакомились с Бьякуей', time_start=388, time_start_pretty='00:06:28', id=5403, hash='01d5b04eaac30eb8', icon='js_preres_url + "/uploads/achievements/icons/5403.jpg"')
        Achievement(category='events', title='Столкновение дерзких', description='Ичиго против Ренджи', time_start=996, time_start_pretty='00:16:36', id=5404, hash='8be5bd722f32ce77', icon='js_preres_url + "/uploads/achievements/icons/5404.jpg"')
        Achievement(category='techniques', title='Шикай', description='Имя духовного меча', time_start=1245, time_start_pretty='00:20:45', id=5405, hash='101ae1b37e1fe928', icon='js_preres_url + "/uploads/achievements/icons/5405.jpg"')
    
    https://jut.su/bleeach/episode-20.html (3):
        Achievement(category='heroes', title='Наречённый Кенпачи', description='Вы познакомились с Зараки', time_start=173, time_start_pretty='00:02:53', id=5413, hash='462468af84ac04ce', icon='js_preres_url + "/uploads/achievements/icons/5413.jpg"')
        Achievement(category='heroes', title='Лисья ухмылка', description='Вы познакомились с Гином', time_start=213, time_start_pretty='00:03:33', id=5414, hash='e0e467aeeb4722e3', icon='js_preres_url + "/uploads/achievements/icons/5414.jpg"')
        Achievement(category='arcs', title='На тот свет', description='Завершите арку временного шинигами', time_start=1298, time_start_pretty='00:21:38', id=5415, hash='8b7bd7aee1812a97', icon='js_preres_url + "/uploads/achievements/icons/5415.jpg"')
    
    https://jut.su/bleeach/episode-21.html (3):
        Achievement(category='places', title='Сообщество душ', description='Добро пожаловать в пригород', time_start=310, time_start_pretty='00:05:10', id=5416, hash='c1bb9bbe2b279cdf', icon='js_preres_url + "/uploads/achievements/icons/5416.jpg"')
        Achievement(category='events', title='Ты не пройдёшь', description='Страж у ворот', time_start=426, time_start_pretty='00:07:06', id=5417, hash='0f838fddc6b69eb9', icon='js_preres_url + "/uploads/achievements/icons/5417.jpg"')
        Achievement(category='events', title='Скрываясь за улыбкой', description='Гин преграждает путь', time_start=1297, time_start_pretty='00:21:37', id=5418, hash='0cc407800fd702f8', icon='js_preres_url + "/uploads/achievements/icons/5418.jpg"')
    
    https://jut.su/bleeach/episode-24.html (5):
        Achievement(category='heroes', title='Очаровательный лейтенант', description='Вы познакомились с Рангику', time_start=513, time_start_pretty='00:08:33', id=5423, hash='badf811540a0624d', icon='js_preres_url + "/uploads/achievements/icons/5423.jpg"')
        Achievement(category='teams', title='Готей 13', description='Хранители Сообщества душ', time_start=1123, time_start_pretty='00:18:43', id=5424, hash='0878a34a4b1c37de', icon='js_preres_url + "/uploads/achievements/icons/5424.jpg"')
        Achievement(category='heroes', title='Безумный исследователь', description='Вы познакомились с Маюри', time_start=1190, time_start_pretty='00:19:50', id=5425, hash='ef89fbc847927475', icon='js_preres_url + "/uploads/achievements/icons/5425.jpg"')
        Achievement(category='heroes', title='Ледяной вундеркинд', description='Вы познакомились с Хицугаей', time_start=1202, time_start_pretty='00:20:02', id=5426, hash='8d21e97d2439c9b3', icon='js_preres_url + "/uploads/achievements/icons/5426.jpg"')
        Achievement(category='heroes', title='Главнокомандующий', description='Вы познакомились с Ямамото', time_start=1244, time_start_pretty='00:20:44', id=5427, hash='65dae88d94c2853b', icon='js_preres_url + "/uploads/achievements/icons/5427.jpg"')
    
    https://jut.su/bleeach/episode-47.html (3):
        Achievement(category='humor', title='Купание с кошкой', description='Отдых после тренировок', time_start=708, time_start_pretty='00:11:48', id=5474, hash='f576fe99d8540790', icon='js_preres_url + "/uploads/achievements/icons/5474.jpg"')
        Achievement(category='events', title='Письмо Айзена', description='За всем стоит Хицугая?', time_start=1071, time_start_pretty='00:17:51', id=5475, hash='30cdc4a0b0dbee78', icon='js_preres_url + "/uploads/achievements/icons/5475.jpg"')
        Achievement(category='events', title='Двойной игрок', description='Хицугая против Гина', time_start=1292, time_start_pretty='00:21:32', id=5476, hash='57135afc778ba53d', icon='js_preres_url + "/uploads/achievements/icons/5476.jpg"')
    """
