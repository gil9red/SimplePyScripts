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
    text = """
    category: "events",
    time_start: 704,
    title: "Ядовитый бутон",
    description: "Высвобождение Заэльаппоро",
    icon: js_preres_url + "/uploads/achievements/icons/5703.jpg",
    id: "5703",
    hash: "11560c9068571116"
    """
    expected = {
        'category': 'events', 'time_start': '704', 'title': 'Ядовитый бутон',
        'description': 'Высвобождение Заэльаппоро',
        'icon': 'js_preres_url + "/uploads/achievements/icons/5703.jpg"',
        'id': '5703', 'hash': '11560c9068571116'
    }
    assert parse_this_anime_achievement(text) == expected

    text = """
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
    expected = [
        {
            'category': 'events', 'time_start': '704',
            'title': 'Ядовитый бутон', 'description': 'Высвобождение Заэльаппоро',
            'icon': 'js_preres_url + "/uploads/achievements/icons/5703.jpg"',
            'id': '5703', 'hash': '11560c9068571116'
        },
        {
            'category': 'events', 'time_start': '1286',
            'title': 'Не изменилась', 'description': 'Нелл не думает сдаваться',
            'icon': 'js_preres_url + "/uploads/achievements/icons/5704.jpg"',
            'id': '5704', 'hash': 'dc3acd1d8af21525'
        }
    ]
    assert parse_this_anime_achievements(text) == expected
    assert get_achievements('https://jut.su/bleeach/episode-193.html')

    for url in [
        'https://jut.su/bleeach/episode-214.html',
        'https://jut.su/bleeach/episode-215.html',
        'https://jut.su/bleeach/episode-216.html',
    ]:
        achievements = get_achievements(url)
        print(f'{url} ({len(achievements)}):')

        for achievement in achievements:
            print(f'    {achievement}')

        print()
    """
    https://jut.su/bleeach/episode-214.html (2):
        {'category': 'humor', 'time_start': '206', 'title': 'Супергеройское вступление', 'description': 'Вы не то аниме смотрите!', 'icon': 'js_preres_url + "/uploads/achievements/icons/5737.jpg"', 'id': '5737', 'hash': '1378bb852797397a'}
        {'category': 'events', 'time_start': '1303', 'title': 'Чужики руками', 'description': 'Подготовка к битве завершена', 'icon': 'js_preres_url + "/uploads/achievements/icons/5738.jpg"', 'id': '5738', 'hash': '5af18fa5d9a6df67'}
    
    https://jut.su/bleeach/episode-215.html (3):
        {'category': 'credits', 'time_start': '89', 'title': 'Shojo S', 'description': 'Посмотрите 10 опенинг', 'icon': 'js_preres_url + "/uploads/achievements/icons/5739.jpg"', 'id': '5739', 'hash': '0f2454a59ffe8e5a'}
        {'category': 'events', 'time_start': '576', 'title': 'Командир ходит первым', 'description': 'Ямамото против Айзена', 'icon': 'js_preres_url + "/uploads/achievements/icons/5740.jpg"', 'id': '5740', 'hash': 'f3cb561798275cd0'}
        {'category': 'events', 'time_start': '1303', 'title': 'Монолог о душе', 'description': 'Улькиорра и Орихиме', 'icon': 'js_preres_url + "/uploads/achievements/icons/5741.jpg"', 'id': '5741', 'hash': '877333633f784067'}
    
    https://jut.su/bleeach/episode-216.html (2):
        {'category': 'events', 'time_start': '468', 'title': 'Наравне?', 'description': 'Новый бой с Улькиоррой', 'icon': 'js_preres_url + "/uploads/achievements/icons/5742.jpg"', 'id': '5742', 'hash': '07ada1f2b8b84316'}
        {'category': 'events', 'time_start': '635', 'title': 'План Бараггана', 'description': 'Вернуть настоящую Каракуру', 'icon': 'js_preres_url + "/uploads/achievements/icons/5743.jpg"', 'id': '5743', 'hash': 'd36c534e102ba3d0'}
    """
