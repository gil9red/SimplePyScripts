#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from db import db_create_backup, Game
from utils_dump import get_parsers, get_funcs_parsers


if __name__ == "__main__":
    for parser in get_parsers():
        print(f"{parser.get_site_name():<25}: {parser.get_game_genres('Dead Space')}")

    # print()
    #
    # for site, get_game_genres in get_funcs_parsers().items():
    #     print(f"{site:<25}: {get_game_genres('Dead Space')}")
    # # ag.ru                    : ['Шутеры', 'Экшены']
    # # gamebomb.ru              : ['Боевик-приключения', 'Шутер']
    # # gamefaqs.gamespot.com    : ['Arcade', 'Shooter', 'Action', 'Third-Person']
    # # gameguru.ru              : ['Экшен', 'Шутер']
    # # gamer.info.com           : ['ужасы', 'action']
    # # gamespot.com             : ['3D', 'Shooter', 'Action', 'Third-Person']
    # # igromania.ru             : ['Боевик', 'Ужасы', 'Боевик от третьего лица']
    # # iwantgames.ru            : []
    # # metacritic.com           : ['Arcade', 'Third-Person', 'Sci-Fi', 'Action', 'Shooter']
    # # mobygames.com            : ['Action']
    # # playground.ru            : ['Ужасы', 'От третьего лица', 'Космос', 'Экшен']
    # # spong.com                : ['Adventure: Survival Horror']
    # # stopgame.ru              : []
    # # store.steampowered.com   : ['Action']
