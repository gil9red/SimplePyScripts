#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from enum import Enum, auto


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


print(Direction)  # <enum 'Direction'>
print(Direction.UP)  # Direction.UP
print(Direction.DOWN)  # Direction.DOWN
print()

print(Direction.UP.value)  # 1
print(Direction.UP == 1)  # False
print(Direction.UP == 2)  # False
print()

direction = Direction.UP
print(direction == Direction.UP)  # True
print(direction == Direction.DOWN)  # False
print()

print(Direction(1))  # Direction.UP
print(Direction(3))  # Direction.LEFT
print()

print(list(Direction))
# [<Direction.UP: 1>, <Direction.DOWN: 2>, <Direction.LEFT: 3>, <Direction.RIGHT: 4>]

print([x for x in Direction])
# [<Direction.UP: 1>, <Direction.DOWN: 2>, <Direction.LEFT: 3>, <Direction.RIGHT: 4>]
