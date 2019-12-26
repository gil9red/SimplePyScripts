#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from db import db_create_backup, Game
from utils_dump import get_parsers, get_funcs_parsers


if __name__ == "__main__":
    for parser in get_parsers():
        parser._need_logs = False
        print(f"{parser.get_site_name():<25}: {parser.get_game_genres('Dead Space')}")

    # ag_ru                    : ['Экшены', 'Шутеры']
    # gamebomb_ru              : ['Боевик-приключения', 'Шутер']
    # gamefaqs_gamespot_com    : ['Action', 'Arcade', 'Shooter', 'Third-Person']
    # gameguru_ru              : ['Экшен', 'Шутер']
    # gamer_info_com           : ['ужасы', 'action']
    # gamespot_com             : ['Action', '3D', 'Shooter', 'Third-Person']
    # igromania_ru             : ['Боевик от третьего лица', 'Боевик', 'Ужасы']
    # iwantgames_ru            : []
    # metacritic_com           : ['Action', 'Shooter', 'Sci-Fi', 'Arcade', 'Third-Person']
    # mobygames_com            : ['Action']
    # playground_ru            : ['От третьего лица', 'Экшен', 'Космос', 'Ужасы']
    # spong_com                : ['Adventure: Survival Horror']
    # stopgame_ru              : []
    # store_steampowered_com   : ['Action']
