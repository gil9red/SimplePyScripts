#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from enum import Enum, auto
from random import choice, choices


class MoveEnum(Enum):
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()


for _ in range(5):
    button = choice(list(MoveEnum))
    print(f"{button:<14} {button.name:<5} {button.value}")

print()
print(choices(list(MoveEnum), k=5))
