#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import enum


class CommandEnum(enum.Enum):
    SEND_PUBLIC_KEY = enum.auto()
    CURRENT_DATETIME = enum.auto()
    CURRENT_TIMESTAMP = enum.auto()
    RANDOM = enum.auto()
    GUID = enum.auto()


if __name__ == '__main__':
    print(CommandEnum)                        # <enum 'CommandEnum'>
    print(CommandEnum.SEND_PUBLIC_KEY)        # CommandEnum.SEND_PUBLIC_KEY
    print(CommandEnum.SEND_PUBLIC_KEY.name)   # SEND_PUBLIC_KEY
    print(CommandEnum.SEND_PUBLIC_KEY.value)  # 1
    print(str(CommandEnum.SEND_PUBLIC_KEY))   # CommandEnum.SEND_PUBLIC_KEY
