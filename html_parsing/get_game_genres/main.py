#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from timeit import default_timer
from threading import Thread
import time
import sys

sys.path.append('genre_translate_file')
import create as create_genre_translate

from db import db_create_backup, Dump
from common_utils import get_parsers, get_games_list, wait, get_logger, AtomicCounter, seconds_to_str, print_parsers
from common import IGNORE_SITE_NAMES

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
    try:
        pauses = [
            ('15 minutes', 15 * 60),
            ('30 minutes', 30 * 60),
            ('45 minutes', 45 * 60),
            ('1 hour', 60 * 60),
        ]
        SITE_NAME = parser.get_site_name()
        timeout = 3                       # 3 seconds
        MAX_TIMEOUT = 10                  # 10 seconds
        TIMEOUT_EVERY_N_GAMES = 50        # Every 50 games
        TIMEOUT_BETWEEN_N_GAMES = 3 * 60  # 3 minutes
        number = 0

        for game_name in games:
            try:
                if Dump.exists(SITE_NAME, game_name):
                    continue

                number += 1

                num_request = 0

                while True:
                    num_request += 1
                    try:
                        if num_request == 1:
                            log.info(f'#{number}. Search genres for {game_name!r} ({SITE_NAME})')
                        else:
                            log.info(f'#{number}. Search genres for {game_name!r} ({SITE_NAME}). '
                                     f'Attempts {num_request}/{max_num_request}')

                        genres = parser.get_game_genres(game_name)
                        log.info(f'#{number}. Found genres {game_name!r} ({SITE_NAME}): {genres}')

                        Dump.add(SITE_NAME, game_name, genres)
                        counter.inc()

                        time.sleep(timeout)
                        break

                    except:
                        log.exception(f'#{number}. Error on request {num_request}/{max_num_request} ({SITE_NAME})')
                        if num_request >= max_num_request:
                            log.info(f'#{number}. Attempts ended for {game_name!r} ({SITE_NAME})')
                            break

                        pause_text, pause_secs = pauses[num_request - 1]
                        log.info(f'#{number}. Pause: {pause_text} secs')
                        time.sleep(pause_secs)

                        timeout += 1
                        if timeout > MAX_TIMEOUT:
                            timeout = MAX_TIMEOUT

                if number % TIMEOUT_EVERY_N_GAMES == 0:
                    log.info(
                        f'#{number}. Pause for every {TIMEOUT_EVERY_N_GAMES} games: {TIMEOUT_BETWEEN_N_GAMES} secs'
                    )
                    time.sleep(TIMEOUT_BETWEEN_N_GAMES)

            except:
                log.exception(f'#{number}. Error by game {game_name!r} ({SITE_NAME})')

    except:
        log.exception(f'Error:')


if __name__ == "__main__":
    parsers = get_parsers()
    print_parsers(parsers, log=lambda *args, **kwargs: log.info(*args, **kwargs))

    while True:
        try:
            log.info(f'Started')
            t = default_timer()

            db_create_backup()

            games = get_games_list()
            log.info(f'Total games: {len(games)}')

            threads = []
            for parser in parsers:
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

        finally:
            log.info('')
