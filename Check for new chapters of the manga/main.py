#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# TODO: костыль для винды, для исправления проблем с исключениями
# при выводе юникодных символов в консоль винды
# Возможно, не только для винды, но и для любой платформы стоит использовать
# эту настройку -- мало какие проблемы могут встретиться
import sys
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter(sys.stdout.encoding)(sys.stdout.detach(), 'backslashreplace')
    sys.stderr = codecs.getwriter(sys.stderr.encoding)(sys.stderr.detach(), 'backslashreplace')


import requests
from config import *


def get_logger(name=__name__, file='log.txt', encoding='utf8'):
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


log = get_logger()


def get_feeds_by_manga_chapters(url_rss: str) -> list:
    import feedparser
    feed = feedparser.parse(url_rss)

    feeds = list()

    for entry in feed.entries:
        title = entry.title

        if title.startswith('Манга '):
            title = title[len('Манга '):]

        elif title.startswith('Взрослая манга '):
            title = title[len('Взрослая манга '):]

        feeds.append(title)

    return feeds


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
            rs = requests.get(url)
            log.debug(repr(rs.text))

            break

        except requests.exceptions.ConnectionError as e:
            log.warning('Ошибка подключения к сети: %s', e)
            log.debug('Через минуту попробую снова...')

            import time
            time.sleep(60)

        except:
            log.exception("При отправке sms произошла ошибка:")
            log.debug('Через 5 минут попробую снова...')

            import time
            time.sleep(5 * 60)


URL_USER_RSS = 'https://grouple.ru/user/rss/315828?filter='
FILE_NAME_LAST_FEED = 'last_feed'


def save_last_feed(feed):
    open(FILE_NAME_LAST_FEED, 'w', encoding='utf-8').write(feed)


if __name__ == '__main__':
    # NOTE: С этим флагом нужно быть осторожным при первом запуске, когда список книг пустой
    notified_by_sms = True

    # Загрузка последней новости
    last_feed = open(FILE_NAME_LAST_FEED, encoding='utf-8').read()

    while True:
        try:
            log.debug('get_feeds_by_manga_chapters')
            log.debug('Last feed: "%s"', last_feed)

            current_feeds = get_feeds_by_manga_chapters(URL_USER_RSS)
            log.debug('current_feeds: %s', current_feeds)

            # Если последняя новость есть в списке текущих новостей
            if last_feed in current_feeds:
                index = current_feeds.index(last_feed)

                # Получаем список новостей после последней новости
                new_feeds = current_feeds[:index]
                if new_feeds:
                    last_feed = new_feeds[0]
                    save_last_feed(last_feed)

                    log.debug('Вышло:')
                    for manga in new_feeds:
                        log.debug('    ' + manga)

                    if notified_by_sms:
                        send_sms(API_ID, TO, 'Новые главы: {}'.format(len(new_feeds)))

                else:
                    log.debug('Новых глав нет')

            else:
                # Считаем что это первый запуск
                last_feed = current_feeds[0]
                log.debug('Первый запуск, запоминаю последнюю главу: "{}"'.format(last_feed))

                save_last_feed(last_feed)

            wait(hours=6)

        except requests.exceptions.ConnectionError as e:
            log.warning('Ошибка подключения к сети: %s', e)
            log.debug('Через минуту попробую снова...')

            import time
            time.sleep(60)

        except:
            log.exception('Непредвиденная ошибка:')
            log.debug('Через 5 минут попробую снова...')

            import time
            time.sleep(5 * 60)
