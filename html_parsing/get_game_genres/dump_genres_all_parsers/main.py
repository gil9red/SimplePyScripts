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
