#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о появлении новых серий аниме Богиня благословляет этот прекрасный мир.

"""


# Чтобы можно было импортировать all_common.py, находящийся уровнем выше
import sys
sys.path.append('..')
sys.path.append('../../online_anidub_com')


from all_common import make_backslashreplace_console, get_logger, simple_send_sms, wait
from get_video_list import search_video_list, get_shorted_names


def my_search_video_list():
    items = search_video_list('Богиня благословляет этот прекрасный мир')
    new_items = get_shorted_names(items)

    log.debug('my_search_video_list\nitems: %s\nnew_items: %s', items, new_items)

    return new_items


make_backslashreplace_console()


log = get_logger('new video Богиня благословляет этот прекрасный мир')


FILE_NAME_CURRENT_ITEMS = 'video'


def save_items(items):
    open(FILE_NAME_CURRENT_ITEMS, mode='w', encoding='utf-8').write(str(items))


if __name__ == '__main__':
    notified_by_sms = True

    # Загрузка текущих элементов
    try:
        import ast
        current_items = ast.literal_eval(open(FILE_NAME_CURRENT_ITEMS, encoding='utf-8').read())

    except:
        current_items = []

    log.debug('Current items(%s): %s', len(current_items), current_items)

    while True:
        try:
            log.debug('get items')

            items = my_search_video_list()
            log.debug('items: %s', items)

            # Если список текущих игр
            if not current_items:
                log.debug('Обнаружен первый запуск')

                current_items = items
                save_items(current_items)

            else:
                new_items = set(items) - set(current_items)
                if new_items:
                    current_items = items
                    save_items(current_items)

                    for item in new_items:
                        text = 'Новая серия "{}"'.format(item)
                        log.debug(text)

                        if notified_by_sms:
                            simple_send_sms(text, log)

                else:
                    log.debug('Изменений нет')

            wait(weeks=2)

        except:
            log.exception('Ошибка:')
            log.debug('Через 5 минут попробую снова...')

            # Wait 5 minutes before next attempt
            import time
            time.sleep(5 * 60)
