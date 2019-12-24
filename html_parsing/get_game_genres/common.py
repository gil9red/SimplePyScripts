#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import unicodedata


def smart_comparing_names(name_1, name_2):
    """
    Функция для сравнивания двух названий игр.
    Возвращает True, если совпадают, иначе -- False.

    """

    # Приведение строк к одному регистру
    name_1 = name_1.lower()
    name_2 = name_2.lower()

    def remove_postfix(text: str, postfix='(dlc)') -> str:
        if text.endswith(postfix):
            text = text[:-len(postfix)]

        return text

    # Удаление символов кроме буквенных, цифр и _: "the witcher®3:___ вася! wild hunt" -> "thewitcher3___васяwildhunt"
    def clear_name(name: str) -> str:
        import re
        return re.sub(r'\W|the', '', name)

    name_1 = remove_postfix(name_1)
    name_2 = remove_postfix(name_2)

    return clear_name(name_1) == clear_name(name_2)


def get_norm_text(node) -> str:
    if not node:
        return ""

    text = node.get_text(strip=True)

    # NFKD ™ превратит в TM, что исказит текст, лучше удалить
    text = text.replace('™', '').replace('©', '').replace('©', '®')

    # https://ru.wikipedia.org/wiki/Юникод#NFKD
    # unicodedata.normalize для удаления \xa0 и подобных символов-заменителей
    return unicodedata.normalize("NFKD", text)


def get_uniques(items: list) -> list:
    return list(set(items))


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/163c91d6882b548c904ad40703dac00c0a64e5a2/logger_example.py#L7
def get_logger(file_name, encoding='utf-8'):
    import os.path
    site = os.path.splitext(os.path.basename(file_name))[0]

    name = 'parser_' + site
    file = 'logs/' + site + '.txt'

    import logging
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] %(filename)s:%(lineno)d %(levelname)-8s %(message)s')

    dir_name = os.path.dirname(file)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    from logging.handlers import RotatingFileHandler
    fh = RotatingFileHandler(file, maxBytes=10_000_000, backupCount=5, encoding=encoding)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    import sys
    sh = logging.StreamHandler(stream=sys.stdout)
    sh.setFormatter(formatter)
    log.addHandler(sh)

    return log


TEST_GAMES = [
    'Hellgate: London',
    'The Incredible Adventures of Van Helsing',
    'Dark Souls: Prepare to Die Edition',
    'Twin Sector',
    'Call of Cthulhu: Dark Corners of the Earth',
]

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'


def _common_test(get_game_genres, sleep=1, max_number=None):
    if max_number is None:
        max_number = len(TEST_GAMES)

    import time

    for name in TEST_GAMES[:max_number]:
        print(f'Search {name!r}...')
        print(f'    Genres: {get_game_genres(name)}\n')

        time.sleep(sleep)
