#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import enum


class CommandEnum(enum.Enum):
    NEW_PUBLIC_KEY = enum.auto()


# TODO: more commands
    # if command == 'CURRENT_DATETIME':
    #     import datetime as DT
    #     return DT.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    #
    # elif command == 'CURRENT_TIMESTAMP':
    #     import datetime as DT
    #     return str(DT.datetime.now().timestamp())
    #
    # elif command == 'RANDOM':
    #     import random
    #     return str(random.randint(0, 1000000))


if __name__ == '__main__':
    print(CommandEnum)                       # <enum 'CommandEnum'>
    print(CommandEnum.NEW_PUBLIC_KEY)        # CommandEnum.NEW_PUBLIC_KEY
    print(CommandEnum.NEW_PUBLIC_KEY.name)   # NEW_PUBLIC_KEY
    print(CommandEnum.NEW_PUBLIC_KEY.value)  # 1
    print(str(CommandEnum.NEW_PUBLIC_KEY))   # CommandEnum.NEW_PUBLIC_KEY
