#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from timeit import default_timer
from threading import Thread
import time
import sys

sys.path.append('genre_translate_file')
import create as create_genre_translate

from db import db_create_backup, Dump, db
from common_utils import get_parsers, get_games_list, wait, get_logger, AtomicCounter, seconds_to_str, print_parsers


IGNORE_SITE_NAMES = ['gamefaqs_gamespot_com']

# Test
USE_FAKE_PARSER = False
if USE_FAKE_PARSER:
    class FakeParser:
        @classmethod
        def get_site_name(cls): return "<test>"

        @staticmethod
        def get_game_genres(game_name):
            if game_name == 'Foo':
                raise Exception('Error')

            return ['RGB-bar', 'Action-bar']

    # Monkey Patch
    def get_parsers():
        return [FakeParser]

    def get_games_list(): return ['Foo', 'Bar', 'Zet']


log = get_logger()
counter = AtomicCounter()


def run_parser(parser, games: list, max_num_request=5):
    pauses = [
        ('15 minutes', 15 * 60),
        ('30 minutes', 30 * 60),
        ('45 minutes', 45 * 60),
        ('1 hour',     60 * 60),
    ]
    site_name = parser.get_site_name()

    for game_name in games:
        if Dump.exists(site_name, game_name):
            continue

        num_request = 0

        while True:
            num_request += 1
            try:
                if num_request == 1:
                    log.info(f'Search genres for {game_name!r} ({site_name})')
                else:
                    log.info(f'Search genres for {game_name!r} ({site_name}). Attempts {num_request}/{max_num_request}')

                genres = parser.get_game_genres(game_name)
                log.info(f'Found genres {game_name!r} ({site_name}): {genres}')

                Dump.add(site_name, game_name, genres)
                counter.inc()

                time.sleep(2)
                break

            except:
                log.exception(f'Error on request {num_request}/{max_num_request}')
                if num_request >= max_num_request:
                    log.info(f'Attempts ended for {game_name!r} ({site_name})')
                    break

                pause_text, pause_secs = pauses[num_request - 1]
                log.info(f'Pause: {pause_text}')
                time.sleep(pause_secs)


if __name__ == "__main__":
    parsers = [x for x in get_parsers() if x.get_site_name() not in IGNORE_SITE_NAMES]
    print_parsers(parsers, log=lambda *args, **kwargs: log.info(*args, **kwargs))

    while True:
        try:
            log.info(f'Started')
            t = default_timer()

            db_create_backup()

            games = get_games_list()
            log.info(f'Total games: {len(games)}')

            threads = []
            for parser in parsers[:1]:
                threads.append(
                    Thread(target=run_parser, args=[parser, games])
                )
            log.info(f'Total parsers/threads: {len(threads)}')
            log.info(f'Ignore parsers ({len(IGNORE_SITE_NAMES)}): {", ".join(IGNORE_SITE_NAMES)}')

            counter.value = 0

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()

            log.info(f'Finished. Added games: {counter.value}. Total games: {Dump.select().count()}. '
                     f'Elapsed time: {seconds_to_str(default_timer() - t)}')

            create_genre_translate.run()

            wait(days=1)

        except:
            log.exception('')
            wait(minutes=15)
