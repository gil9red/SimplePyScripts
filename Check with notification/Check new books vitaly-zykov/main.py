#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о появлении новых книг Зыкова.

"""


# Чтобы можно было импортировать all_common.py, находящийся уровнем выше
import sys
sys.path.append('..')


from all_common import make_backslashreplace_console, get_logger, simple_send_sms, wait


make_backslashreplace_console()


log = get_logger('vitaly-zykov new books')


def get_books():
    import requests
    rs = requests.get('http://vitaly-zykov.ru/knigi')

    from bs4 import BeautifulSoup
    root = BeautifulSoup(rs.content, 'lxml')

    return [x.text.strip().replace('"', '') for x in root.select('.book_tpl > h3')]


FILE_NAME_CURRENT_BOOKS = 'books'


if __name__ == '__main__':
    # NOTE: С этим флагом нужно быть осторожным при первом запуске, когда список книг пустой
    notified_by_sms = True

    # Загрузка текущих книг
    import ast
    current_books = ast.literal_eval(open(FILE_NAME_CURRENT_BOOKS, encoding='utf-8').read())
    log.debug('Current books: %s', current_books)

    while True:
        try:
            log.debug('get books')

            books = get_books()
            log.debug('books: %s', books)

            new_books = set(books) - set(current_books)
            if new_books:
                current_books = books
                open(FILE_NAME_CURRENT_BOOKS, mode='w', encoding='utf-8').write(str(current_books))

                for book in new_books:
                    text = 'Появилась новая книга Зыкова: "{}"'.format(book)
                    log.debug(text)

                    if notified_by_sms:
                        simple_send_sms(text, log)

            else:
                log.debug('Новых книг нет')

            wait(weeks=1)

        except:
            log.exception('Ошибка:')
            log.debug('Через 5 минут попробую снова...')

            # Wait 5 minutes before next attempt
            import time
            time.sleep(5 * 60)
