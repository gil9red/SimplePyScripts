#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Этот скрипт анализирует файл с списком игр, заполняет sqlite базу пройденными и просмотренными играми, ищет цену
этим играм и заполняет указывает их играм.

"""


from common import (
    parse_game_name, steam_search_game_price_list, smart_comparing_names,
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
