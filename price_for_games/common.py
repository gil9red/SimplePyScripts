#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


DB_FILE_NAME = 'games.sqlite'
FINISHED = 'Finished'
FINISHED_WATCHED = 'Finished watched'

# TODO: доработать идею
# https://docs.python.org/3.4/library/sqlite3.html
# import sqlite3
# connect = sqlite3.connect(DB_FILE_NAME)
# cursor = connect.cursor()


def create_connect():
    import sqlite3
    return sqlite3.connect(DB_FILE_NAME)


# NOTE: пример получения данных с конвертированием времени в строковой вид
# get_game_sql = '''
#     SELECT name, price, strftime('%Y-%m-%d', modify_date)
#     FROM game
#     WHERE kind = ?
#     ORDER BY name
# '''


import re
PARSE_GAME_NAME_PATTERN = re.compile(r'(\d+(, ?\d+)+)|(\d+ *?- *?\d+)|([MDCLXVI]+(, ?[MDCLXVI]+)+)',
                                     flags=re.IGNORECASE)


def parse_game_name(game_name):
    match = PARSE_GAME_NAME_PATTERN.search(game_name)
    if match is None:
        return [game_name]

    seq_str = match.group(0)
    short_name = game_name.replace(seq_str, '').strip()

    if ',' in seq_str:
        seq = seq_str.replace(' ', '').split(',')

    elif '-' in seq_str:
        seq = seq_str.replace(' ', '').split('-')
        if len(seq) > 2:
            print('Unknown seq str = "{}".'.format(seq_str))
        else:
            seq = tuple(map(int, seq))
            seq = tuple(range(seq[0], seq[1] + 1))
    else:
        print('Unknown seq str = "{}".'.format(seq_str))
        return [game_name]

    # Сразу проверяем номер игры в серии и если она первая, то не добавляем в названии ее номер
    return [short_name if str(num) == '1' else '{} {}'.format(short_name, num) for num in seq]


def search_game_price_list(name):
    # category1 = 998 (Game)
    url = 'http://store.steampowered.com/search/?category1=998&os=win&supportedlang=english&term=' + name

    game_price_list = list()

    import requests
    rs = requests.get(url)
    if not rs.ok:
        print('Что-то пошло не так: {}\n{}'.format(rs.status_code, rs.text))
        return game_price_list

    from bs4 import BeautifulSoup
    root = BeautifulSoup(rs.content, 'lxml')

    for div in root.select('.search_result_row'):
        name = div.select_one('.title').text.strip()

        # Ищем тег скидки
        if div.select_one('.search_discount > span'):
            price = div.select_one('.search_price > span > strike').text.strip()
        else:
            price = div.select_one('.search_price').text.strip()

        # Если цены нет (например, игра еще не продается)
        if not price:
            price = None
        else:
            # Если в цене нет цифры считаем что это "Free To Play" или что-то подобное
            import re
            match = re.search(r'\d', price)
            if not match:
                price = 0

        game_price_list.append((name, price))

    return game_price_list


def clear_name(name):
    import re
    return re.sub(r'[^\w]', '', name).replace('_', '')


def smart_comparing_names(name_1, name_2):
    # Приведение строк к одному регистру
    name_1 = name_1.lower()
    name_2 = name_2.lower()

    # Удаление символов кроме буквенных и цифр: "the witcher®3:___ вася! wild hunt" -> "thewitcher3васяwildhunt"
    name_1 = clear_name(name_1)
    name_2 = clear_name(name_2)

    # TODO: REMOVE THIS
    if name_1 == name_2:
        print(name_1, name_2)

    return name_1 == name_2