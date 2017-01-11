#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# Подсчитать стоимость игр:
# https://gist.github.com/gil9red/50283a567f05c8cae9531d573f905ae2

from common import (
    parse_game_name, search_game_price_list, smart_comparing_names,
    DB_FILE_NAME, FINISHED, FINISHED_WATCHED,
    create_connect, get_games_list, append_games_to_base, fill_price_of_games, settings
)

# Создание базы и таблицы
connect = create_connect()
cursor = connect.cursor()

# Имя игры и ее вид должны быть уникальными
cursor.execute('''
CREATE TABLE IF NOT EXISTS Game (
    name TEXT,
    price TEXT,
    modify_date TIMESTAMP,
    kind TEXT,

    CONSTRAINT game_pk PRIMARY KEY (name, kind)
);
''')

connect.commit()

while True:
    # Перед выполнением, запоминаем дату и время, чтобы иметь потом представление когда
    # в последний раз выполнялось заполнение списка
    from datetime import datetime
    settings.last_run_date = datetime.today()

    finished_game_list, finished_watched_game_list = get_games_list()
    print("Пройденных игр {}, просмотренных игр: {}".format(len(finished_game_list), len(finished_watched_game_list)))

    # Добавление в базу новых игр
    append_games_to_base(connect, finished_game_list, finished_watched_game_list)

    # Заполнение цен игр
    fill_price_of_games(connect)

    # Every 3 days
    import time
    time.sleep(60 * 60 * 24 * 3)


# print('\n\n')
# # for row in c.execute('SELECT * FROM game where price is not null'):
# for row in c.execute('SELECT * FROM game'):
#     print(row)

# NOTE: пусть коннект живет все время работы скрипта
# TODO: или нужно испоьлдзование коннекта обернуть в блоки типа with и вызывать автоматом, после выполнения
# блока кода
# NOTE: По идеи, соединение и так прервется, когда скрипт завершится
# connect.close()
