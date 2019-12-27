#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT
from threading import Thread

from db import db_create_backup, Game, db
from utils_dump import get_parsers, get_games_list, wait


# Monkey patch
def get_games_list():
    import json
    return json.load(open('games.json', encoding='utf-8'))

def run_parser(parser, games: list):
    # from threading import current_thread
    # print(current_thread(), parser, games[:5])

    for game_name in games:
        genres = ["RPG", "Action"]
        Game.add(parser.get_site_name(), game_name, genres)


if __name__ == "__main__":
    # while True:
    #     print(f'Started at {DT.datetime.now():%d/%m/%Y %H:%M:%S}\n')
    #
    #     db_create_backup()

    games = get_games_list()

    for parser in get_parsers():
        thread = Thread(target=run_parser, args=[parser, games])
        thread.start()

        # parser._need_logs = False
        # print(f"{parser.get_site_name():<25}: {parser.get_game_genres('Dead Space')}")
