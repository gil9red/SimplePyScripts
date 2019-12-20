#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from glob import glob
import importlib.util
import os
import sys
from typing import Dict, Callable

# For import common.py
sys.path.append('..')


def module_from_file(file_path):
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_parsers() -> Dict[str, Callable]:
    data = dict()

    for file_name in glob('../*.py'):
        module = module_from_file(file_name)
        if 'get_game_genres' not in dir(module):
            continue

        data[module.__name__.replace('_', '.')] = module.get_game_genres

    return data


if __name__ == "__main__":
    for site, get_game_genres in get_parsers().items():
        print(f"{site:<25}: {get_game_genres('Dead Space')}")

    # ag.ru                    : ['Шутеры', 'Экшены']
    # gamebomb.ru              : ['Боевик-приключения', 'Шутер']
    # gamefaqs.gamespot.com    : ['Arcade', 'Shooter', 'Action', 'Third-Person']
    # gameguru.ru              : ['Экшен', 'Шутер']
    # gamer.info.com           : ['ужасы', 'action']
    # gamespot.com             : ['3D', 'Shooter', 'Action', 'Third-Person']
    # igromania.ru             : ['Боевик', 'Ужасы', 'Боевик от третьего лица']
    # iwantgames.ru            : []
    # metacritic.com           : ['Arcade', 'Third-Person', 'Sci-Fi', 'Action', 'Shooter']
    # mobygames.com            : ['Action']
    # playground.ru            : ['Ужасы', 'От третьего лица', 'Космос', 'Экшен']
    # spong.com                : ['Adventure: Survival Horror']
    # stopgame.ru              : []
    # store.steampowered.com   : ['Action']
