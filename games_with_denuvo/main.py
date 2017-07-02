#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для периодического сбора данных и занесения в базу.

"""


def wait(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
    from datetime import timedelta, datetime
    today = datetime.today()
    timeout_date = today + timedelta(
        days=days, seconds=seconds, microseconds=microseconds,
        milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks
    )

    while today <= timeout_date:
        def str_timedelta(td):
            # Remove ms
            td = str(td)
            if '.' in td:
                td = td[:td.index('.')]

            return td

        left = timeout_date - today
        left = str_timedelta(left)

        print('\r' * 100, end='')
        print('До следующего запуска осталось {}'.format(left), end='')

        import sys
        sys.stdout.flush()

        # Delay 1 seconds
        import time
        time.sleep(1)

        today = datetime.today()

    print('\r' * 100, end='')
    print('\n')


from common import *


if __name__ == '__main__':
    # connect = create_connect()
    # connect.execute("DROP TABLE IF EXISTS Game")
    # connect.commit()

    init_db()

    # NOTE: С этим флагом нужно быть осторожным при первом запуске, когда база пуста,
    # ведь на каждую добавленную взломанную игру отправится уведомление по смс
    notified_by_sms = True

    while True:
        try:
            log.debug('get_games_with_denuvo')

            from games_with_denuvo import get_games_with_denuvo
            games = get_games_with_denuvo()
            log.debug('games: %s', games)

            append_list_games(games, notified_by_sms)

            wait(days=3)

        except Exception:
            log.exception('Ошибка:')
            log.debug('Через 5 минут попробую снова...')

            # Wait 5 minutes before next attempt
            import time
            time.sleep(5 * 60)
