#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о новых сериях Черный клевер

"""


# Чтобы можно было импортировать all_common.py, находящийся уровнем выше
import sys
sys.path.append('..')
sys.path.append('../../html_parsing')

from all_common import make_backslashreplace_console, get_logger, simple_send_sms, wait
from anivost_org import get_last_series

make_backslashreplace_console()


import time
import requests


log = get_logger('Check new series Черный клевер')


def get_last_value() -> str:
    last_value = get_last_series('https://anivost.org/24-chernyy-klever.html')
    return str(last_value)


FILE_NAME_LAST_VALUE = 'last_value'


def update_file_data(value: str):
    open(FILE_NAME_LAST_VALUE, mode='w', encoding='utf-8').write(value)


if __name__ == '__main__':
    notified_by_sms = True

    try:
        last_value = open(FILE_NAME_LAST_VALUE, encoding='utf-8').read()
    except:
        last_value = ''

    while True:
        try:
            log.debug('Запрос последней серии')
            log.debug('Последнее значение: %s', last_value if last_value else '<null>')

            current_last_series = get_last_value()
            log.debug('Текущее значение: %s', current_last_series)

            # Если предыдущий ранг не был известен, например при первом запуске скрипта
            if not last_value:
                log.debug('Обнаружен первый запуск')

                last_value = current_last_series
                update_file_data(last_value)

            else:
                if last_value != current_last_series:
                    text = f'Добавлена новая серия: {current_last_series} (предыдущая {last_value})'
                    log.debug(text)

                    # Обновление последнего значения
                    last_value = current_last_series
                    update_file_data(last_value)

                    if notified_by_sms:
                        simple_send_sms(text, log)

                else:
                    log.debug('Значение не изменился')

            wait(days=1)

        except requests.exceptions.ConnectionError as e:
            log.warning('Ошибка подключения к сети: %s', e)
            log.debug('Через минуту попробую снова...')

            time.sleep(60)

        except:
            log.exception('Непредвиденная ошибка:')
            log.debug('Через 5 минут попробую снова...')

            time.sleep(5 * 60)
