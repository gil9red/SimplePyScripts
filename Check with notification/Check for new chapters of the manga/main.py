#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# Чтобы можно было импортировать all_common.py, находящийся уровнем выше
import sys
sys.path.append('..')

import requests

from all_common import make_backslashreplace_console, get_logger, simple_send_sms, wait


make_backslashreplace_console()


log = get_logger('new_chapters_manga')


def get_feeds_by_manga_chapters(url_rss: str) -> list:
    rss_text = requests.get(url_rss).text

    import feedparser
    feed = feedparser.parse(rss_text)

    feeds = list()

    for entry in feed.entries:
        title = entry.title

        if title.startswith('Манга '):
            title = title[len('Манга '):]

        elif title.startswith('Взрослая манга '):
            title = title[len('Взрослая манга '):]

        feeds.append(title)

    return feeds


URL_USER_RSS = 'https://grouple.co/user/rss/315828?filter='
FILE_NAME_LAST_FEED = 'last_feed'


def save_last_feed(feed):
    open(FILE_NAME_LAST_FEED, 'w', encoding='utf-8').write(feed)


if __name__ == '__main__':
    notified_by_sms = True

    # Загрузка последней новости
    try:
        last_feed = open(FILE_NAME_LAST_FEED, encoding='utf-8').read()
    except:
        last_feed = ""

    while True:
        try:
            log.debug('get_feeds_by_manga_chapters')
            log.debug('Last feed: "%s"', last_feed)

            current_feeds = get_feeds_by_manga_chapters(URL_USER_RSS)
            log.debug('current_feeds: %s', current_feeds)

            if not last_feed or last_feed not in current_feeds:
                # Считаем что это первый запуск
                last_feed = current_feeds[0]
                log.debug('Первый запуск, запоминаю последнюю главу: "{}"'.format(last_feed))

                save_last_feed(last_feed)

            # Если последняя новость есть в списке текущих новостей
            else:
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
                        text = 'Новые главы: {}'.format(len(new_feeds))
                        simple_send_sms(text, log)

                else:
                    log.debug('Новых глав нет')

            # wait(hours=6)
            wait(days=7)

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
