#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import logging
import re

from base64 import b64decode

from common import session


DEBUG = False

logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format='[%(asctime)s] %(levelname)-8s %(message)s',
)

RE_BASE64 = re.compile(r'eval\( *Base64.decode\( *"(.+?)" *\) *\);')
RE_SOME_ACHIV_STR = re.compile(r'some_achiv_str *= *"(.+?)";')
RE_BRACE_CONTENT = re.compile(r'\{(.+?)\}', flags=re.DOTALL)


def parse_this_anime_achievement(anime_achievement: str) -> dict[str, str]:
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

    values = dict()
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

    return values


def parse_this_anime_achievements(some_achiv_str: str) -> list[dict[str, str]]:
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
        parse_this_anime_achievement(value)
        for value in RE_BRACE_CONTENT.findall(some_achiv_str)
    ]


def get_achievements(url: str) -> list[dict[str, str]]:
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

    return parse_this_anime_achievements(some_achiv_str)


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
        {'category': 'credits', 'time_start': '100', 'title': 'Asterisk', 'description': 'Посмотрите 1 опенинг', 'icon': 'js_preres_url + "/uploads/achievements/icons/5371.jpg"', 'id': '5371', 'hash': 'ae60172ce6e31e2e'}
        {'category': 'heroes', 'time_start': '144', 'title': 'Жнец душ', 'description': 'Вы познакомились с Рукией', 'icon': 'js_preres_url + "/uploads/achievements/icons/5372.jpg"', 'id': '5372', 'hash': '364b2421c7fe6046'}
        {'category': 'heroes', 'time_start': '223', 'title': 'Заступник', 'description': 'Вы познакомились с Ичиго', 'icon': 'js_preres_url + "/uploads/achievements/icons/5373.jpg"', 'id': '5373', 'hash': 'e02379c16879ce52'}
        {'category': 'events', 'time_start': '1246', 'title': 'Временный шинигами', 'description': 'Примеряя роль проводника душ', 'icon': 'js_preres_url + "/uploads/achievements/icons/5374.jpg"', 'id': '5374', 'hash': 'a9af11fc7a5a5fc6'}
    
    https://jut.su/bleeach/episode-16.html (3):
        {'category': 'heroes', 'time_start': '388', 'title': 'Глава Кучики', 'description': 'Вы познакомились с Бьякуей', 'icon': 'js_preres_url + "/uploads/achievements/icons/5403.jpg"', 'id': '5403', 'hash': '01d5b04eaac30eb8'}
        {'category': 'events', 'time_start': '996', 'title': 'Столкновение дерзких', 'description': 'Ичиго против Ренджи', 'icon': 'js_preres_url + "/uploads/achievements/icons/5404.jpg"', 'id': '5404', 'hash': '8be5bd722f32ce77'}
        {'category': 'techniques', 'time_start': '1245', 'title': 'Шикай', 'description': 'Имя духовного меча', 'icon': 'js_preres_url + "/uploads/achievements/icons/5405.jpg"', 'id': '5405', 'hash': '101ae1b37e1fe928'}
    
    https://jut.su/bleeach/episode-20.html (3):
        {'category': 'heroes', 'time_start': '173', 'title': 'Наречённый Кенпачи', 'description': 'Вы познакомились с Зараки', 'icon': 'js_preres_url + "/uploads/achievements/icons/5413.jpg"', 'id': '5413', 'hash': '462468af84ac04ce'}
        {'category': 'heroes', 'time_start': '213', 'title': 'Лисья ухмылка', 'description': 'Вы познакомились с Гином', 'icon': 'js_preres_url + "/uploads/achievements/icons/5414.jpg"', 'id': '5414', 'hash': 'e0e467aeeb4722e3'}
        {'category': 'arcs', 'time_start': '1298', 'title': 'На тот свет', 'description': 'Завершите арку временного шинигами', 'icon': 'js_preres_url + "/uploads/achievements/icons/5415.jpg"', 'id': '5415', 'hash': '8b7bd7aee1812a97'}
    
    https://jut.su/bleeach/episode-21.html (3):
        {'category': 'places', 'time_start': '310', 'title': 'Сообщество душ', 'description': 'Добро пожаловать в пригород', 'icon': 'js_preres_url + "/uploads/achievements/icons/5416.jpg"', 'id': '5416', 'hash': 'c1bb9bbe2b279cdf'}
        {'category': 'events', 'time_start': '426', 'title': 'Ты не пройдёшь', 'description': 'Страж у ворот', 'icon': 'js_preres_url + "/uploads/achievements/icons/5417.jpg"', 'id': '5417', 'hash': '0f838fddc6b69eb9'}
        {'category': 'events', 'time_start': '1297', 'title': 'Скрываясь за улыбкой', 'description': 'Гин преграждает путь', 'icon': 'js_preres_url + "/uploads/achievements/icons/5418.jpg"', 'id': '5418', 'hash': '0cc407800fd702f8'}
    
    https://jut.su/bleeach/episode-24.html (5):
        {'category': 'heroes', 'time_start': '513', 'title': 'Очаровательный лейтенант', 'description': 'Вы познакомились с Рангику', 'icon': 'js_preres_url + "/uploads/achievements/icons/5423.jpg"', 'id': '5423', 'hash': 'badf811540a0624d'}
        {'category': 'teams', 'time_start': '1123', 'title': 'Готей 13', 'description': 'Хранители Сообщества душ', 'icon': 'js_preres_url + "/uploads/achievements/icons/5424.jpg"', 'id': '5424', 'hash': '0878a34a4b1c37de'}
        {'category': 'heroes', 'time_start': '1190', 'title': 'Безумный исследователь', 'description': 'Вы познакомились с Маюри', 'icon': 'js_preres_url + "/uploads/achievements/icons/5425.jpg"', 'id': '5425', 'hash': 'ef89fbc847927475'}
        {'category': 'heroes', 'time_start': '1202', 'title': 'Ледяной вундеркинд', 'description': 'Вы познакомились с Хицугаей', 'icon': 'js_preres_url + "/uploads/achievements/icons/5426.jpg"', 'id': '5426', 'hash': '8d21e97d2439c9b3'}
        {'category': 'heroes', 'time_start': '1244', 'title': 'Главнокомандующий', 'description': 'Вы познакомились с Ямамото', 'icon': 'js_preres_url + "/uploads/achievements/icons/5427.jpg"', 'id': '5427', 'hash': '65dae88d94c2853b'}
    
    https://jut.su/bleeach/episode-47.html (3):
        {'category': 'humor', 'time_start': '708', 'title': 'Купание с кошкой', 'description': 'Отдых после тренировок', 'icon': 'js_preres_url + "/uploads/achievements/icons/5474.jpg"', 'id': '5474', 'hash': 'f576fe99d8540790'}
        {'category': 'events', 'time_start': '1071', 'title': 'Письмо Айзена', 'description': 'За всем стоит Хицугая?', 'icon': 'js_preres_url + "/uploads/achievements/icons/5475.jpg"', 'id': '5475', 'hash': '30cdc4a0b0dbee78'}
        {'category': 'events', 'time_start': '1292', 'title': 'Двойной игрок', 'description': 'Хицугая против Гина', 'icon': 'js_preres_url + "/uploads/achievements/icons/5476.jpg"', 'id': '5476', 'hash': '57135afc778ba53d'}
    """
