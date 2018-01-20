#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о изменении ранга на ru.stackoverflow.

"""


# Чтобы можно было импортировать all_common.py, находящийся уровнем выше
import sys
sys.path.append('..')


from all_common import make_backslashreplace_console, get_logger, simple_send_sms, wait


make_backslashreplace_console()


import time
import requests


log = get_logger('Check new rank ru.stackoverflow')


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
    notified_by_sms = True

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
                    text = 'Изменился ранг: {} -> {} ({})'.format(last_rank, rank, reputation)
                    log.debug(text)

                    # Обновление последнего ранга
                    last_rank = rank
                    update_file_data(last_rank)

                    if notified_by_sms:
                        simple_send_sms(text, log)

                else:
                    log.debug('Ранг не изменился')

            wait(weeks=1)

        except requests.exceptions.ConnectionError as e:
            log.warning('Ошибка подключения к сети: %s', e)
            log.debug('Через минуту попробую снова...')

            time.sleep(60)

        except:
            log.exception('Непредвиденная ошибка:')
            log.debug('Через 5 минут попробую снова...')

            time.sleep(5 * 60)
