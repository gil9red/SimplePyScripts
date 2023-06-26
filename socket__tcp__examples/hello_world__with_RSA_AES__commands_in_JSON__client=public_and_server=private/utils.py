#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import enum


class CommandEnum(enum.Enum):
    CURRENT_DATETIME = enum.auto()
    CURRENT_TIMESTAMP = enum.auto()
    RANDOM = enum.auto()
    GUID = enum.auto()


FILE_NAME_PUBLIC_KEY = "keys/public.pem"
FILE_NAME_PRIVATE_KEY = "keys/private.pem"


if __name__ == "__main__":
    print(CommandEnum)
