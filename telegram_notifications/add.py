#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import Union

from db import Notification
from config import CHAT_ID
from common import TypeEnum


def add(name: str, message: str, type: Union[TypeEnum, str] = TypeEnum.INFO):
    if not CHAT_ID:
        raise Exception('Нужно заполнить "CHAT_ID.txt"!')

    if not isinstance(type, TypeEnum):
        type = TypeEnum[type]

    Notification.add(
        chat_id=CHAT_ID,
        name=name,
        message=message,
        type=type,
    )


if __name__ == '__main__':
    add('TEST', 'Hello World! Привет мир!')
    add('', 'Hello World! Привет мир!')
