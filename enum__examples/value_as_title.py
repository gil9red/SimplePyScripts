#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from enum import Enum, auto
from random import choice


class KeyboardEnum(Enum):
    ALL = auto()
    YES = auto()
    NO = auto()
    CANCEL = auto()
    GET_ALL = auto()
    SEND_ALL = auto()

    def title(self):
        return self.name.replace("_", " ")


print(KeyboardEnum.GET_ALL)  # KeyboardEnum.GET_ALL
print(KeyboardEnum.GET_ALL.title())  # GET ALL
print()

button = choice(list(KeyboardEnum))
print(f'{button}: "{button.title()}"')

print(KeyboardEnum.SEND_ALL)
