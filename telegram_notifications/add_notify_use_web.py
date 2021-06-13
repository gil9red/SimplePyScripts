#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import Union

import requests

from common import TypeEnum
from config import HOST, PORT


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
