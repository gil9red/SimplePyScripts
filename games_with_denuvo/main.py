#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для периодического сбора данных и занесения в базу.

"""


# TODO: костыль для винды, для исправления проблем с исключениями
# при выводе юникодных символов в консоль винды
# Возможно, не только для винды, но и для любой платформы стоит использовать
# эту настройку -- мало какие проблемы могут встретиться
import sys
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter(sys.stdout.encoding)(sys.stdout.detach(), 'backslashreplace')
    sys.stderr = codecs.getwriter(sys.stderr.encoding)(sys.stderr.detach(), 'backslashreplace')


def wait(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
    from datetime import timedelta, datetime
    today = datetime.today()
    timeout_date = today + timedelta(
        days=days, seconds=seconds, microseconds=microseconds,
        milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks
    )

    while today <= timeout_date:
        def str_timedelta(td):
            mm, ss = divmod(td.seconds, 60)
            hh, mm = divmod(mm, 60)
            return "%d:%02d:%02d" % (hh, mm, ss)

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

    while True:
        try:
            log.debug('get_games_with_denuvo')

            from games_with_denuvo import get_games_with_denuvo
            games = get_games_with_denuvo()
            log.debug('games: %s', games)

            append_list_games(games)

            wait(weeks=1)

        except Exception:
            log.exception('Ошибка:')
            log.debug('Через 5 минут попробую снова...')

            # Wait 5 minutes before next attempt
            import time
            time.sleep(5 * 60)
