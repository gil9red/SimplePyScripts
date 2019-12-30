#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from timeit import default_timer
from threading import Thread
import time

from db import db_create_backup, Game, db
from utils_dump import get_parsers, get_games_list, wait, get_logger, AtomicCounter, seconds_to_str


log = get_logger()
counter = AtomicCounter()


def run_parser(parser, games: list):
    for game_name in games:
        site_name = parser.get_site_name()
        if Game.exists(site_name, game_name):
            continue

        log.info(f'Search genres for {game_name!r} ({site_name})')

        while True:
            try:
                genres = parser.get_game_genres(game_name)
                log.info(f'Found genres {game_name!r} ({site_name}): {genres}')

                Game.add(parser.get_site_name(), game_name, genres)
                counter.inc()

                time.sleep(1)
                break

            except:
                log.exception("Error")
                wait(minutes=5)


if __name__ == "__main__":
    while True:
        log.info(f'Started')
        t = default_timer()

        db_create_backup()

        games = get_games_list()
        log.info(f'Total games: {len(games)}')

        threads = []
        for parser in get_parsers():
            threads.append(
                Thread(target=run_parser, args=[parser, games])
            )
        log.info(f'Total parsers/threads: {len(threads)}')

        counter.value = 0

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        log.info(f'Finished. Processed games: {counter.value}. '
                 f'Elapsed time: {seconds_to_str(default_timer() - t)}')

        wait(days=1)
