#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import importlib.util
import sys
import threading

from glob import glob
from pathlib import Path
from typing import Union

# For import parsers/*
sys.path.append('parsers')


from common import DIR_LOGS, IGNORE_SITE_NAMES


def module_from_file(file_path: str):
    module_name = Path(file_path).stem
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if module_name not in sys.modules:
        sys.modules[module_name] = module

    return module


def get_parsers() -> list:
    items = []

    for file_name in glob('parsers/*.py'):
        module = module_from_file(file_name)
        for attr in dir(module):
            if not attr.endswith('_Parser'):
                continue

            cls = getattr(module, attr)
            parser = cls.instance()
            if parser.get_site_name() not in IGNORE_SITE_NAMES:
                items.append(parser)

    return items


# Parser from https://github.com/gil9red/played_games/blob/f23777a1368f9124450bedac036791068d8ca099/mini_played_games_parser.py#L7
def parse_played_games(text: str, silence: bool=False) -> dict:
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

    platforms = dict()
    platform = None

    for line in text.splitlines():
        line = line.rstrip()
        if not line:
            continue

        flag = line[:2]
        if flag not in FLAG_BY_CATEGORY and line.endswith(':'):
            platform_name = line[:-1]

            platform = {
                FINISHED_GAME: [],
                NOT_FINISHED_GAME: [],
                FINISHED_WATCHED: [],
                NOT_FINISHED_WATCHED: [],
            }
            platforms[platform_name] = platform

            continue

        if not platform:
            continue

        category_name = FLAG_BY_CATEGORY.get(flag)
        if not category_name:
            if not silence:
                print('Странный формат строки: "{}"'.format(line))
            continue

        category = platform[category_name]

        game_name = line[2:]
        for game in parse_game_name(game_name):
            if game in category:
                if not silence:
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


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/8fa9b9c23d10b5ee7ff0161da997b463f7a861bf/wait/wait.py#L7
def wait(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
    from datetime import timedelta, datetime
    from itertools import cycle
    import sys
    import time

    try:
        progress_bar = cycle('|/-\\|/-\\')

        today = datetime.today()
        timeout_date = today + timedelta(
            days=days, seconds=seconds, microseconds=microseconds,
            milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks
        )

        def str_timedelta(td: timedelta) -> str:
            td = str(td)

            # Remove ms
            # 0:01:40.123000 -> 0:01:40
            if '.' in td:
                td = td[:td.rindex('.')]

            # 0:01:40 -> 00:01:40
            if td.startswith('0:'):
                td = '00:' + td[2:]

            return td

        while today <= timeout_date:
            left = timeout_date - today
            left = str_timedelta(left)

            print('\r' + ' ' * 100 + '\r', end='')
            print('[{}] Time left to wait: {}'.format(next(progress_bar), left), end='')
            sys.stdout.flush()

            # Delay 1 seconds
            time.sleep(1)

            today = datetime.today()

        print('\r' + ' ' * 100 + '\r', end='')

    except KeyboardInterrupt:
        print()
        print('Waiting canceled')


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/163c91d6882b548c904ad40703dac00c0a64e5a2/logger_example.py#L7
def get_logger(name='dump.txt', encoding='utf-8'):
    Path(DIR_LOGS).mkdir(parents=True, exist_ok=True)

    file = DIR_LOGS + '/' + name

    import logging
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] %(levelname)-8s %(message)s')

    from logging.handlers import RotatingFileHandler
    fh = RotatingFileHandler(file, maxBytes=10_000_000, backupCount=5, encoding=encoding)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    import sys
    sh = logging.StreamHandler(stream=sys.stdout)
    sh.setFormatter(formatter)
    log.addHandler(sh)

    return log


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/c06ff5fb6a0abfb5a41652f71d7adf7ee414e4c8/multithreading__threading__examples/atomic_counter.py#L14
class AtomicCounter:
    def __init__(self, initial=0):
        self.value = initial
        self._lock = threading.Lock()

    def inc(self, num=1):
        with self._lock:
            self.value += num
            return self.value


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/f0403620f7948306ad9e34a373f2aabc0237fb2a/seconds_to_str.py
def seconds_to_str(seconds: Union[int, float]) -> str:
    hh, mm = divmod(seconds, 3600)
    mm, ss = divmod(mm, 60)
    return "%02d:%02d:%02d" % (hh, mm, ss)


def print_parsers(parsers: list, log=print):
    max_width = len(max([x.get_site_name() for x in parsers], key=len))
    fmt_str = '    {:<%d} : {}' % max_width
    items = [
        fmt_str.format(parser.get_site_name(), parser.__class__)
        for parser in parsers
    ]

    log(f'Parsers ({len(parsers)}):\n' + "\n".join(items))


if __name__ == "__main__":
    items = get_games_list()
    print(f'Games ({len(items)}): {", ".join(items[:5])}...')
    # Games (743): 35MM, 60 Seconds!, A Bird Story, A Plague Tale: Innocence, A Story About My Uncle...

    print()

    parsers = get_parsers()
    print_parsers(parsers)
    # Parsers (14):
    #     ag_ru                  : <class 'ag_ru.AgRu_Parser'>
    #     gamebomb_ru            : <class 'gamebomb_ru.GamebombRu_Parser'>
    #     gamefaqs_gamespot_com  : <class 'gamefaqs_gamespot_com.GamefaqsGamespotCom_Parser'>
    #     gameguru_ru            : <class 'gameguru_ru.GameguruRu_Parser'>
    #     gamer_info_com         : <class 'gamer_info_com.GamerInfoCom_Parser'>
    #     gamespot_com           : <class 'gamespot_com.GamespotCom_Parser'>
    #     igromania_ru           : <class 'igromania_ru.IgromaniaRu_Parser'>
    #     iwantgames_ru          : <class 'iwantgames_ru.IwantgamesRu_Parser'>
    #     metacritic_com         : <class 'metacritic_com.MetacriticCom_Parser'>
    #     mobygames_com          : <class 'mobygames_com.MobygamesCom_Parser'>
    #     playground_ru          : <class 'playground_ru.PlaygroundRu_Parser'>
    #     spong_com              : <class 'spong_com.SpongCom_Parser'>
    #     stopgame_ru            : <class 'stopgame_ru.StopgameRu_Parser'>
    #     store_steampowered_com : <class 'store_steampowered_com.StoreSteampoweredCom_Parser'>

    print()

    game = 'Dead Space'
    print(f'Search genres for {game!r}:')

    for parser in parsers:
        parser._need_logs = False
        try:
            print(f"    {parser.get_site_name():<25}: {parser.get_game_genres(game)}")
        except Exception as e:
            print(f"    {parser.get_site_name():<25}: {e}")
    """
        ag_ru                    : ['Экшены', 'Шутеры']
        gamebomb_ru              : ['Шутер', 'Боевик-приключения']
        gameguru_ru              : ['Шутер', 'Хоррор', 'Экшен']
        gamer_info_com           : ('Connection aborted.', ConnectionResetError(10054, 'Удаленный хост принудительно разорвал существующее подключение', None, 10054, None))
        gamespot_com             : []
        igromania_ru             : ['Хоррор', 'Экшен', 'FPS']
        iwantgames_ru            : []
        metacritic_com           : ('Connection aborted.', ConnectionResetError(10054, 'Удаленный хост принудительно разорвал существующее подключение', None, 10054, None))
        mobygames_com            : ['Action']
        playground_ru            : []
        spong_com                : ['Adventure: Survival Horror']
        squarefaction_ru         : ['TPS', 'Action', 'Survival Horror']
        stopgame_ru              : []
        store_steampowered_com   : []
    """
