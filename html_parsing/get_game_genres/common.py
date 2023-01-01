#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT
import re
from pathlib import Path


# SOURCE: https://github.com/gil9red/price_of_games/blob/9311f9cbc6b9e57d0308436e3dbf3e524f23ef74/app_parser/utils.py
def smart_comparing_names(name_1: str, name_2: str) -> bool:
    """
    Функция для сравнивания двух названий игр.
    Возвращает True, если совпадают, иначе -- False.

    """

    # Приведение строк к одному регистру
    name_1 = name_1.lower()
    name_2 = name_2.lower()

    def remove_postfix(text: str) -> str:
        for postfix in ('dlc', 'expansion'):
            if text.endswith(postfix):
                return text[:-len(postfix)]
        return text

    # Удаление символов кроме буквенных, цифр и _: "the witcher®3:___ вася! wild hunt" -> "thewitcher3___васяwildhunt"
    def clear_name(name: str) -> str:
        return re.sub(r'\W', '', name)

    name_1 = clear_name(name_1)
    name_1 = remove_postfix(name_1)

    name_2 = clear_name(name_2)
    name_2 = remove_postfix(name_2)

    return name_1 == name_2


def get_uniques(items: list) -> list:
    return list(set(items))


def pretty_path(path: str) -> str:
    return str(Path(path).resolve())


def get_current_datetime_str(fmt='%Y-%m-%d_%H%M%S') -> str:
    return DT.datetime.now().strftime(fmt)


# SOURCE: https://github.com/django/django/blob/03dbdfd9bbbbd0b0172aad648c6bbe3f39541137/django/utils/text.py#L221
def get_valid_filename(s):
    """
    Return the given string converted to a string that can be used for a clean
    filename. Remove leading and trailing spaces; convert other spaces to
    underscores; and remove anything that is not an alphanumeric, dash,
    underscore, or dot.
    >>> get_valid_filename("john's portrait in 2004.jpg")
    'johns_portrait_in_2004.jpg'
    """
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)


USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.00'

DIR = Path(__file__).resolve().parent
DIR_ERRORS = str(DIR / 'errors')
DIR_LOGS = str(DIR / 'logs')

NEED_LOGS = True
LOG_FORMAT = '[%(asctime)s] %(levelname)-8s %(message)s'


TEST_GAMES = [
    'Hellgate: London',
    'The Incredible Adventures of Van Helsing',
    'Dark Souls: Prepare to Die Edition',
    'Twin Sector',
    'Call of Cthulhu: Dark Corners of the Earth',
]


def _common_test(get_game_genres, sleep=1, max_number=None):
    if max_number is None:
        max_number = len(TEST_GAMES)

    import time

    for name in TEST_GAMES[:max_number]:
        print(f'Search {name!r}...')
        print(f'    Genres: {get_game_genres(name)}\n')

        time.sleep(sleep)


IGNORE_SITE_NAMES = [
    'gamefaqs_gamespot_com',  # NOTE: Проверяет на ботов, дает доступ на разрешение не парсить :)
    'gamer_info_com',  # NOTE: Не работает то ли, из-за версии HTTP/2, то ли из-за российского IP
    'metacritic_com',  # NOTE: Не работает то ли, из-за версии HTTP/2, то ли из-за российского IP
]
