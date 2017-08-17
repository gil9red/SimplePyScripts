#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о появлении новых видео Gorgeous Freeman.

"""


# При выводе юникодных символов в консоль винды
# Возможно, не только для винды, но и для любой платформы стоит использовать
# эту настройку -- мало какие проблемы могут встретиться
import sys
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter(sys.stdout.encoding)(sys.stdout.detach(), 'backslashreplace')
    sys.stderr = codecs.getwriter(sys.stderr.encoding)(sys.stderr.detach(), 'backslashreplace')


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


log = get_logger('new video Gorgeous Freeman')


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


def get_video_list():
    text = 'Gorgeous Freeman - '

    import requests
    rs = requests.get('https://www.youtube.com/user/antoine35DeLak/search?query=' + text)
    log.debug('rs: %s', rs)

    from bs4 import BeautifulSoup
    root = BeautifulSoup(rs.content, 'lxml')

    video_title_list = [x.text for x in root.select('.yt-lockup-title > a')]
    log.debug('video_title_list[%s]: %s', len(video_title_list), video_title_list)

    # Get video list and filter by <text>
    return list(filter(lambda x: x.startswith(text), video_title_list))


FILE_NAME_CURRENT_NUMBER_VIDEO = 'current_number_video'


if __name__ == '__main__':
    # NOTE: С этим флагом нужно быть осторожным при первом запуске, когда список книг пустой
    notified_by_sms = True

    try:
        current_number_video = int(open(FILE_NAME_CURRENT_NUMBER_VIDEO, encoding='utf-8').read())
    except:
        current_number_video = 0

    while True:
        try:
            log.debug('get video number')
            log.debug('current_number_video: %s', current_number_video)

            video_list = get_video_list()
            number_video = len(video_list)

            log.debug('video list[%s]: %s', number_video, sorted(video_list))

            if number_video > current_number_video:
                current_number_video = number_video
                open(FILE_NAME_CURRENT_NUMBER_VIDEO, mode='w', encoding='utf-8').write(str(current_number_video))

                text = 'Появилось новое видео Gorgeous Freeman'
                log.debug(text)

                if notified_by_sms:
                    send_sms(API_ID, TO, text)

            elif number_video < current_number_video:
                text = 'Случилось странное: видео по Gorgeous Freeman меньше чем было запомнено'
                log.debug(text)

                if notified_by_sms:
                    send_sms(API_ID, TO, text)

            else:
                log.debug('Новых видео нет')

            wait(weeks=1)

        except requests.exceptions.ConnectionError as e:
            log.warning('Ошибка подключения к сети: %s', e)
            log.debug('Через минуту попробую снова...')

            time.sleep(60)

        except:
            log.exception('Непредвиденная ошибка:')
            log.debug('Через 5 минут попробую снова...')

            time.sleep(5 * 60)
