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


def module_from_file(file_path: str):
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if module_name not in sys.modules:
        sys.modules[module_name] = module

    return module


def get_funcs_parsers() -> Dict[str, Callable]:
    data = dict()

    for file_name in glob('../*.py'):
        module = module_from_file(file_name)
        if 'get_game_genres' not in dir(module):
            continue

        data[module.__name__] = module.get_game_genres

    return data


def get_parsers() -> list:
    items = []

    for file_name in glob('../*.py'):
        module = module_from_file(file_name)
        for attr in dir(module):
            if not attr.endswith('_Parser'):
                continue

            cls = getattr(module, attr)
            items.append(
                cls.instance()
            )

    return items


# SOURCE: https://github.com/gil9red/price_of_games/blob/5432514a3322d359ca8ef509f5ef173ce6969203/common.py#L367
def parse_played_games(text: str) -> dict:
    """
    Функция для парсинга списка игр.
    """

    FINISHED_GAME = 'FINISHED_GAME'
    NOT_FINISHED_GAME = 'NOT_FINISHED_GAME'
    FINISHED_WATCHED = 'FINISHED_WATCHED'
    NOT_FINISHED_WATCHED = 'NOT_FINISHED_WATCHED'

    FLAG_BY_CATEGORY = {
        '  ': FINISHED_GAME,
        '- ': NOT_FINISHED_GAME,
        ' -': NOT_FINISHED_GAME,
        ' @': FINISHED_WATCHED,
        '@ ': FINISHED_WATCHED,
        '-@': NOT_FINISHED_WATCHED,
        '@-': NOT_FINISHED_WATCHED,
    }

    # Регулярка вытаскивает выражения вида: 1, 2, 3 или 1-3, или римские цифры: III, IV
    import re
    PARSE_GAME_NAME_PATTERN = re.compile(
        r'(\d+(, *?\d+)+)|(\d+ *?- *?\d+)|([MDCLXVI]+(, ?[MDCLXVI]+)+)',
        flags=re.IGNORECASE
    )

    def parse_game_name(game_name: str) -> list:
        """
        Функция принимает название игры и пытается разобрать его, после возвращает список названий.
        У некоторых игр в названии может указываться ее части или диапазон частей, поэтому для правильного
        составления списка игр такие случаи нужно обрабатывать.
        Пример:
            "Resident Evil 4, 5, 6" -> ["Resident Evil 4", "Resident Evil 5", "Resident Evil 6"]
            "Resident Evil 1-3"     -> ["Resident Evil", "Resident Evil 2", "Resident Evil 3"]
            "Resident Evil 4"       -> ["Resident Evil 4"]
        """

        match = PARSE_GAME_NAME_PATTERN.search(game_name)
        if match is None:
            return [game_name]

        seq_str = match.group(0)

        # "Resident Evil 4, 5, 6" -> "Resident Evil"
        # For not valid "Trollface Quest 1-7-8" -> "Trollface Quest"
        index = game_name.index(seq_str)
        base_name = game_name[:index].strip()

        seq_str = seq_str.replace(' ', '')

        if ',' in seq_str:
            # '1,2,3' -> ['1', '2', '3']
            seq = seq_str.split(',')

        elif '-' in seq_str:
            seq = seq_str.split('-')

            # ['1', '7'] -> [1, 7]
            seq = list(map(int, seq))

            # [1, 7] -> ['1', '2', '3', '4', '5', '6', '7']
            seq = list(map(str, range(seq[0], seq[1] + 1)))

        else:
            return [game_name]

        # Сразу проверяем номер игры в серии и если она первая, то не добавляем в названии ее номер
        return [base_name if num == '1' else base_name + " " + num for num in seq]

    from collections import OrderedDict
    platforms = OrderedDict()
    platform = None

    for line in text.splitlines():
        line = line.rstrip()
        if not line:
            continue

        if line[0] not in ' -@' and line[1] not in ' -@' and line.endswith(':'):
            platform_name = line[:-1]

            platform = OrderedDict()
            platform[FINISHED_GAME] = list()
            platform[NOT_FINISHED_GAME] = list()
            platform[FINISHED_WATCHED] = list()
            platform[NOT_FINISHED_WATCHED] = list()

            platforms[platform_name] = platform

            continue

        if not platform:
            continue

        flag = line[:2]
        category_name = FLAG_BY_CATEGORY.get(flag)
        if not category_name:
            print('Странный формат строки: "{}"'.format(line))
            continue

        category = platform[category_name]

        game_name = line[2:]
        for game in parse_game_name(game_name):
            if game in category:
                print('Предотвращено добавление дубликата игры "{}"'.format(game))
                continue

            category.append(game)

    return platforms


# SOURCE: https://github.com/gil9red/price_of_games/blob/5432514a3322d359ca8ef509f5ef173ce6969203/common.py#L482
def get_games_list() -> list:
    import requests
    rs = requests.get('https://gist.github.com/gil9red/2f80a34fb601cd685353')

    from bs4 import BeautifulSoup
    root = BeautifulSoup(rs.content, 'html.parser')
    href = root.select_one('.file-actions > a')['href']

    from urllib.parse import urljoin
    raw_url = urljoin(rs.url, href)

    rs = requests.get(raw_url)
    content_gist = rs.text

    platforms = parse_played_games(content_gist)

    # Пройденные игры
    finished_game_list = platforms['PC']['FINISHED_GAME']

    # Просмотренные игры
    finished_watched_game_list = platforms['PC']['FINISHED_WATCHED']

    return sorted(set(finished_game_list + finished_watched_game_list))


if __name__ == "__main__":
    items = get_games_list()
    print(f'Games ({len(items)}): {", ".join(items[:5])}...')
    # Games (743): 35MM, 60 Seconds!, A Bird Story, A Plague Tale: Innocence, A Story About My Uncle...

    print()
    quit()

    for parser in get_parsers():
        print(f"{parser.get_site_name():<25}: {parser.__class__}")

    # ag_ru                    : <class 'ag_ru.AgRu_Parser'>
    # gamebomb_ru              : <class 'gamebomb_ru.GamebombRu_Parser'>
    # gamefaqs_gamespot_com    : <class 'gamefaqs_gamespot_com.GamefaqsGamespotCom_Parser'>
    # gameguru_ru              : <class 'gameguru_ru.GameguruRu_Parser'>
    # gamer_info_com           : <class 'gamer_info_com.GamerInfoCom_Parser'>
    # gamespot_com             : <class 'gamespot_com.GamespotCom_Parser'>
    # igromania_ru             : <class 'igromania_ru.IgromaniaRu_Parser'>
    # iwantgames_ru            : <class 'iwantgames_ru.IwantgamesRu_Parser'>
    # metacritic_com           : <class 'metacritic_com.MetacriticCom_Parser'>
    # mobygames_com            : <class 'mobygames_com.MobygamesCom_Parser'>
    # playground_ru            : <class 'playground_ru.PlaygroundRu_Parser'>
    # spong_com                : <class 'spong_com.SpongCom_Parser'>
    # stopgame_ru              : <class 'stopgame_ru.StopgameRu_Parser'>
    # store_steampowered_com   : <class 'store_steampowered_com.StoreSteampoweredCom_Parser'>

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
    # # ag_ru                    : ['Шутеры', 'Экшены']
    # # gamebomb_ru              : ['Боевик-приключения', 'Шутер']
    # # gamefaqs_gamespot_com    : ['Arcade', 'Shooter', 'Action', 'Third-Person']
    # # gameguru_ru              : ['Экшен', 'Шутер']
    # # gamer_info_com           : ['ужасы', 'action']
    # # gamespot_com             : ['3D', 'Shooter', 'Action', 'Third-Person']
    # # igromania_ru             : ['Боевик', 'Ужасы', 'Боевик от третьего лица']
    # # iwantgames_ru            : []
    # # metacritic_com           : ['Arcade', 'Third-Person', 'Sci-Fi', 'Action', 'Shooter']
    # # mobygames_com            : ['Action']
    # # playground_ru            : ['Ужасы', 'От третьего лица', 'Космос', 'Экшен']
    # # spong_com                : ['Adventure: Survival Horror']
    # # stopgame_ru              : []
    # # store_steampowered_com   : ['Action']
