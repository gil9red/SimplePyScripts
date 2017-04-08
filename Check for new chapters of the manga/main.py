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
    from datetime import timedelta
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


def send_sms(api_id: str, to: str, text: str):
    # Отправляю смс на номер
    url = 'https://sms.ru/sms/send?api_id={api_id}&to={to}&text={text}'.format(
        api_id=api_id,
        to=to,
        text=text
    )
    print(repr(url))

    import requests
    rs = requests.get(url)
    print(rs.text)


if __name__ == '__main__':
    # Загрузка последних новостей из файла
    import ast
    current_feeds = ast.literal_eval(open(FILE_NAME_CURRENT_FEEDS, encoding='utf-8').read())
    print(current_feeds)

    # Флаг служит для того, чтобы при первом запуске скрипта, при пустом списке глав в файле <FILE_NAME_CURRENT_FEEDS>
    # скрипт не реагировал на "новые главы"
    first_run = len(current_feeds) == 0

    while True:
        try:
            from datetime import datetime
            today = datetime.today()
            print(today)

            new_feeds = get_feeds_by_manga_chapters(URL_USER_RSS)
            print(new_feeds)

            # NOTE: Тоже самое можно сделать через цикл и новый список
            new_manga = set(new_feeds) - set(current_feeds)

            # Если что-то появилось новое, сохраняем новости
            if new_manga:
                current_feeds = new_feeds
                open(FILE_NAME_CURRENT_FEEDS, 'w', encoding='utf-8').write(str(current_feeds))

                if not first_run:
                    print('Вышло:')
                    for manga in new_manga:
                        print('    ' + manga)

                    send_sms(API_ID, TO, 'Новые главы: {}'.format(len(new_manga)))

                first_run = False

            else:
                print('Новых глав нет')

            print()

            wait(hours=5)

        except Exception:
            import traceback
            print('Ошибка:')
            print(traceback.format_exc())

            print('Через 5 минут попробую снова...')

            # Wait 5 minutes before next attempt
            import time
            time.sleep(5 * 60)
