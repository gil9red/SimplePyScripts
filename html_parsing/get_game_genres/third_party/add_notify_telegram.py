#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/38857704e0821002c21e6840015cc3c0d1dd9b57/telegram_notifications/add_notify_use_web.py


import time
import requests


HOST = '127.0.0.1'
PORT = 10016

URL = f'http://{HOST}:{PORT}/add_notify'


def add_notify(name: str, message: str, type='INFO'):
    data = {
        'name': name,
        'message': message,
        'type': type,
    }

    # Попытки
    attempts_timeouts = [1, 5, 10, 30, 60]

    while True:
        try:
            rs = requests.post(URL, json=data)
            rs.raise_for_status()
            return

        except Exception as e:
            # Если закончились попытки
            if not attempts_timeouts:
                raise e

            timeout = attempts_timeouts.pop(0)
            time.sleep(timeout)


if __name__ == '__main__':
    add_notify('TEST', 'Hello World! Привет мир!')
    add_notify('', 'Hello World! Привет мир!')
    add_notify('Ошибка!', 'Hello World! Привет мир!', 'ERROR')
