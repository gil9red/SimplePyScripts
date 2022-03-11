#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import time
import requests


HOST = '127.0.0.1'
PORT = 10016

URL = f'http://{HOST}:{PORT}/add_notify'


def add_notify(
        name: str,
        message: str,
        type: str = 'INFO',
        url: str = None,
        has_delete_button: bool = False,
):
    data = {
        'name': name,
        'message': message,
        'type': type,
        'url': url,
        'has_delete_button': has_delete_button,
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
    add_notify('TEST', 'With url-button!', url='https://example.com/')
    add_notify('TEST', 'With delete-button!', has_delete_button=True)
    add_notify('TEST', 'With url and delete buttons!', url='https://example.com/', has_delete_button=True)
