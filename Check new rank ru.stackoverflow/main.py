#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о изменении ранга на ru.stackoverflow.

"""


def make_backslashreplace_console():
    # При выводе юникодных символов в консоль винды
    # Возможно, не только для винды, но и для любой платформы стоит использовать
    # эту настройку -- мало какие проблемы могут встретиться
    import sys
    if sys.platform == 'win32':
        import codecs

        try:
            sys.stdout = codecs.getwriter(sys.stdout.encoding)(sys.stdout.detach(), 'backslashreplace')
            sys.stderr = codecs.getwriter(sys.stderr.encoding)(sys.stderr.detach(), 'backslashreplace')

        except AttributeError:
            # ignore "AttributeError: '_io.BufferedWriter' object has no attribute 'encoding'"
            pass


make_backslashreplace_console()


import time
import requests


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


from config import *


def get_logger(name, file='log.txt', encoding='utf8'):
    import sys
    import logging

    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] %(filename)s[LINE:%(lineno)d] %(levelname)-8s %(message)s')

    fh = logging.FileHandler(file, encoding=encoding)
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(logging.DEBUG)

    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    log.addHandler(fh)
    log.addHandler(ch)

    return log


log = get_logger('Check new rank ru.stackoverflow')


def send_sms(api_id: str, to: str, text: str):
    log.debug('Отправка sms: "%s"', text)

    # Отправляю смс на номер
    url = 'https://sms.ru/sms/send?api_id={api_id}&to={to}&text={text}'.format(
        api_id=api_id,
        to=to,
        text=text
    )
    log.debug(repr(url))

    while True:
        try:
            import requests
            rs = requests.get(url)
            log.debug(repr(rs.text))

            break

        except:
            log.exception("При отправке sms произошла ошибка:")
            log.debug('Через 5 минут попробую снова...')

            # Wait 5 minutes before next attempt
            import time
            time.sleep(5 * 60)


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/ae8b728e9fa2a9094e99283a103151173e8eaf3a/stackoverflow/user_rank_and_reputation.py
def get_user_rank_and_reputation() -> (str, str):
    url = 'https://stackexchange.com/leagues/filter-users/355/AllTime/2015-03-27/?filter=gil9red&sort=reputationchange'

    import requests
    rs = requests.get(url)
    text = rs.text
    # print(text)

    import re
    match = re.search('>#(.+)</span> all time rank', text)
    rank = match.group(1)

    match = re.search('>(.+)</span> all time reputation', text)
    reputation = match.group(1).replace(',', '')

    return rank, reputation


FILE_NAME_LAST_RANK = 'last_rank'


def update_file_data(value: str):
    open(FILE_NAME_LAST_RANK, mode='w', encoding='utf-8').write(value)


if __name__ == '__main__':
    notified_by_sms = False

    try:
        last_rank = open(FILE_NAME_LAST_RANK, encoding='utf-8').read()
    except:
        last_rank = ''

    while True:
        try:
            log.debug('get rank and reputation')
            log.debug('last_rank: %s', last_rank if last_rank else '<null>')

            rank, reputation = get_user_rank_and_reputation()

            log.debug('current rank: %s, reputation: %s', rank, reputation)

            # Если предыдущий ранг не был известен, например при первом запуске скрипта
            if not last_rank:
                last_rank = rank
                update_file_data(last_rank)

            else:
                if last_rank != rank:
                    text = 'Изменился ранг: {} -> {}'.format(last_rank, rank)
                    log.debug(text)

                    # Обновление последнего ранга
                    last_rank = rank
                    update_file_data(last_rank)

                    if notified_by_sms:
                        send_sms(API_ID, TO, text)

                else:
                    log.debug('Ранг не изменился')

            # TODO: вернуть обратно
            # wait(weeks=1)
            wait(days=1)

        except requests.exceptions.ConnectionError as e:
            log.warning('Ошибка подключения к сети: %s', e)
            log.debug('Через минуту попробую снова...')

            time.sleep(60)

        except:
            log.exception('Непредвиденная ошибка:')
            log.debug('Через 5 минут попробую снова...')

            time.sleep(5 * 60)
