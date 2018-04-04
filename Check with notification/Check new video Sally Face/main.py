#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о появлении новых видео Sally Face.

"""


# Чтобы можно было импортировать all_common.py, находящийся уровнем выше
import sys
sys.path.append('..')


from all_common import make_backslashreplace_console, get_logger, simple_send_sms, wait


make_backslashreplace_console()


log = get_logger('new video Sally Face')


def get_video_list():
    text = 'Sally Face #'
    url = 'https://www.youtube.com/user/HellYeahPlay/search?query=' + text

    import requests
    rs = requests.get(url)
    log.debug('rs: %s', rs)

    from bs4 import BeautifulSoup
    root = BeautifulSoup(rs.content, 'lxml', from_encoding='utf-8')

    video_title_list = [x.text for x in root.select('.yt-lockup-title > a')]
    # log.debug('video_title_list[%s]: %s', len(video_title_list), video_title_list)
    log.debug('video_title_list[%s]', len(video_title_list))

    # Get video list and filter by <text>
    return list(filter(lambda x: text in x, video_title_list))


FILE_NAME_CURRENT_NUMBER_VIDEO = 'current_number_video'


def save_current_number_video(current_number_video):
    open(FILE_NAME_CURRENT_NUMBER_VIDEO, mode='w', encoding='utf-8').write(str(current_number_video))


if __name__ == '__main__':
    import time
    import requests

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

            if not current_number_video:
                log.debug('Обнаружен первый запуск')

                current_number_video = number_video
                save_current_number_video(current_number_video)

            else:
                if number_video == current_number_video:
                    log.debug('Новых видео нет')

                else:
                    if number_video > current_number_video:
                        text = 'Появилось новое видео Sally Face'
                    else:
                        text = 'Случилось странное: видео по Sally Face меньше чем было запомнено'

                    log.debug(text)

                    current_number_video = number_video
                    save_current_number_video(current_number_video)

                    if notified_by_sms:
                        simple_send_sms(text, log)

            wait(weeks=1)

        except requests.exceptions.ConnectionError as e:
            log.warning('Ошибка подключения к сети: %s', e)
            log.debug('Через минуту попробую снова...')

            time.sleep(60)

        except:
            log.exception('Непредвиденная ошибка:')
            log.debug('Через 5 минут попробую снова...')

            time.sleep(5 * 60)
