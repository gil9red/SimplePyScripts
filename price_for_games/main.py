#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# Подсчитать стоимость игр:
# https://gist.github.com/gil9red/50283a567f05c8cae9531d573f905ae2

from common import (
    parse_game_name, search_game_price_list, smart_comparing_names,
    DB_FILE_NAME, FINISHED, FINISHED_WATCHED
)

#
# Создание базы и таблицы
#

# https://docs.python.org/3.4/library/sqlite3.html
import sqlite3
conn = sqlite3.connect(DB_FILE_NAME)
c = conn.cursor()

# Имя игры и ее вид должны быть уникальными
c.execute('''CREATE TABLE IF NOT EXISTS Game (
    name text,
    price text,
    modify_date integer,
    kind text,

    CONSTRAINT game_pk PRIMARY KEY (name, kind)
);
''')

#
# Скачивание списка игр, вытаскивание из него игр
#

# Пройденные игры
finished_game_list = list()

# Просмотренные игры
finished_watched_game_list = list()

# TODO: убрать кеширование
# Кеширование
import os
if not os.path.exists('gist_games'):
    import requests

    rs = requests.get('https://gist.github.com/gil9red/2f80a34fb601cd685353')

    from bs4 import BeautifulSoup

    root = BeautifulSoup(rs.content, 'lxml')
    href = root.select_one('.file-actions > a')['href']

    from urllib.parse import urljoin

    raw_url = urljoin(rs.url, href)
    print(raw_url)

    # Чтобы при тестировании, при каждом запуске не парсить, лучше скачать и работать
    # уже с самим файлом, отрабатывая алгоритм
    # Сохранение указанного url в файл
    from urllib.request import urlretrieve
    urlretrieve(raw_url, 'gist_games')


with open('gist_games', encoding='utf-8') as f:
    found_pc = False

    # Перебор строк файла
    for line in f:
        # Удаление пустых символов справа (пробелы, переводы на следующую строку и т.п.)
        line = line.rstrip()

        # Если строка пустая
        if not line.strip():
            continue

        # Проверка, что первым символом не может быть флаг для игр и что последним символом будет :
        # Т.е. ищем признак платформы
        if line[0] not in [' ', '-', '@'] and line.endswith(':'):
            # Если встретили PC
            found_pc = line == 'PC:'
            continue

        name = line[2:].rstrip()
        games = parse_game_name(name)

        # Теперь, осталось добавить игру
        if found_pc:
            # Пройденные игры
            if line.startswith('  '):
                finished_game_list += games

            # Просмотренные игры
            elif line.startswith('@ ') or line.startswith(' @'):
                finished_watched_game_list += games

print(len(finished_game_list))
print(len(finished_watched_game_list))

#
# Добавление игр в таблицу базы
#


def insert_game(name, kind):
    c.execute("INSERT OR IGNORE INTO Game VALUES (?,NULL,NULL,?)", (name, kind))

# Добавлени в базу пройденных игр
for name in finished_game_list:
    insert_game(name, FINISHED)

# Добавлени в базу просмотренных игр
for name in finished_watched_game_list:
    insert_game(name, FINISHED_WATCHED)

# Save (commit) the changes
conn.commit()

#
# Получение игр без указанной цены, указание цены
#

# Перебор игр и указание их цены
# Перед перебором собираем все игры и удаляем дубликаты (игры могут и просмотренными, и пройденными)
# заодно список кортежей из одного имени делаем просто списом имен
games_list = set(game for (game,) in c.execute('SELECT name FROM game where price is null').fetchall())
for game in games_list:
    game_price = None

    # Поищем игру и ее цену
    game_price_list = search_game_price_list(game)
    for name, price in game_price_list:
        # Если нашли игру, запоминаем цену и прерываем сравнение с другими найденными играми
        if smart_comparing_names(game, name):
            game_price = price
            break

    if game_price == 0 or game_price is None:
        # TODO: заполнять вручную или искать на других сайтах цену
        print('Не получилось найти цену игры {}, price is {}'.format(game, game_price))
        continue

    print('Нашли игру: {} -> {} : {}\n'.format(game, name, price))

    import time
    timestamp = int(time.time())
    c.execute("UPDATE Game SET price = ?, modify_date = ? WHERE name = ?", (price, timestamp, game))

    time.sleep(3)

conn.commit()


# print('\n\n')
# # for row in c.execute('SELECT * FROM game where price is not null'):
# for row in c.execute('SELECT * FROM game'):
#     print(row)

conn.close()
