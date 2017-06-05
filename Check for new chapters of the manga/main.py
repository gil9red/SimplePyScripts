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
    import requests
    rss_text = requests.get(url_rss).text

    import feedparser
    feed = feedparser.parse(rss_text)

    feeds = list()

    for entry in feed.entries:
        url = entry.link
        title = entry.title

        if 'readmanga' in url:
            title = title[len('Манга '):]

        elif 'mintmanga' in url:
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


if __name__ == '__main__':
    # Загрузка последних новостей из файла
    import ast
    current_feeds = ast.literal_eval(open(FILE_NAME_CURRENT_FEEDS, encoding='utf-8').read())
    log.debug('Feeds from "%s": %s', FILE_NAME_CURRENT_FEEDS, current_feeds)

    # Флаг служит для того, чтобы при первом запуске скрипта, при пустом списке глав в файле <FILE_NAME_CURRENT_FEEDS>
    # скрипт не реагировал на "новые главы"
    first_run = len(current_feeds) == 0

    while True:
        try:
            log.debug('get_feeds_by_manga_chapters')

            new_feeds = get_feeds_by_manga_chapters(URL_USER_RSS)
            log.debug('new_feeds: %s', new_feeds)

            # NOTE: Тоже самое можно сделать через цикл и новый список
            new_manga = set(new_feeds) - set(current_feeds)

            # Если что-то появилось новое, сохраняем новости
            if new_manga:
                current_feeds = new_feeds
                open(FILE_NAME_CURRENT_FEEDS, 'w', encoding='utf-8').write(str(current_feeds))

                if not first_run:
                    log.debug('Вышло:')
                    for manga in new_manga:
                        log.debug('    ' + manga)

                    send_sms(API_ID, TO, 'Новые главы: {}'.format(len(new_manga)))

                first_run = False

            else:
                log.debug('Новых глав нет')

            log.debug("")

            wait(hours=5)

        except Exception:
            log.exception('Ошибка:')
            log.debug('Через 5 минут попробую снова...')

            # Wait 5 minutes before next attempt
            import time
            time.sleep(5 * 60)
