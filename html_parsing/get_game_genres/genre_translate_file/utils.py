#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os


SMS_API_ID = os.getenv('SMS_API_ID')
SMS_SEND_TO = os.getenv('SMS_SEND_TO')


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/157b188116ced699b76986420cdc8378e05296d8/Check%20with%20notification/all_common.py#L57
def send_sms(text: str, log):
    if not SMS_API_ID or not SMS_SEND_TO:
        log.warning('Переменные окружения SMS_API_ID или SMS_SEND_TO не указаны, отправка СМС невозможна!')
        return

    log.info('Отправка sms: "%s"', text)

    # Отправляю смс на номер
    url = 'https://sms.ru/sms/send?api_id={api_id}&to={to}&text={text}'.format(
        api_id=SMS_API_ID,
        to=SMS_SEND_TO,
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
