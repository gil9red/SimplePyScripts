#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys

from pathlib import Path
from typing import Union

import requests

sys.path.append(str(Path(__file__).parent.parent))
from telegram_notifications.common import TypeEnum
from telegram_notifications.config import HOST, PORT


URL = f'http://{HOST}:{PORT}/add_notify'


def add_notify(name: str, message: str, type: Union[TypeEnum, str] = TypeEnum.INFO):
    data = {
        'name': name,
        'message': message,
        'type': type.value,
    }

    rs = requests.post(URL, json=data)
    rs.raise_for_status()


if __name__ == '__main__':
    add_notify('TEST', 'Hello World! Привет мир!')
    add_notify('', 'Hello World! Привет мир!')
    add_notify('Ошибка!', 'Hello World! Привет мир!', TypeEnum.ERROR)
