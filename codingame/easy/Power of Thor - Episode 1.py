#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
# ---
# Hint: You can use the debug stream to print initialTX and initialTY, if Thor seems not follow your orders.

# light_x: the X position of the light of power
# light_y: the Y position of the light of power
# initial_tx: Thor's starting X position
# initial_ty: Thor's starting Y position
light_x, light_y, initial_tx, initial_ty = [int(i) for i in input().split()]

DIRECTION_DICT = {
    (-1, 0): "W",
    (0, -1): "N",
    (1, 0): "E",
    (0, 1): "S",

    (-1, -1): "NW",
    (1, -1): "NE",
    (1, 1): "SE",
    (-1, 1): "SW",
}

x, y = initial_tx, initial_ty
dx, dy = 0, 0
complete_x, complete_y = False, False

# game loop
while True:
    # The remaining amount of turns Thor can move. Do not remove this line.
    remaining_turns = int(input())

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    # A single line providing the move to be made: N NE E SE S SW W or NW
    # print("SE")

    # Проверяем, что герой не находится на одной горизонтали с кругом
    if not complete_x:
        # Круг находится ниже по вертинали
        if light_y > y:
            dy = 1

        # Круг находится выше по вертинали
        elif light_y < y:
            dy = -1
        else:
            dy = 0

        # Если круг находится справа от героя
        if light_x > x:
            dx = 1

        # Если круг находится слева от героя
        elif light_x < x:
            dx = -1
        else:
            dx = 0
            complete_x = True

    # Проверяем, что герой не находится на одной вертикали с кругом
    if not complete_y:
        # Круг находится справа по горизонтали
        if light_x > x:
            dx = 1

        # Круг находится слева по горизонтали
        elif light_x < x:
            dx = -1
        else:
            dx = 0

        # Круг находится ниже по вертинали
        if light_y > y:
            dy = 1

        # Круг находится выше по вертинали
        elif light_y < y:
            dy = -1
        else:
            dy = 0
            complete_y = True

    if complete_x and complete_y:
        print("Finish", file=sys.stderr)
        continue

    x, y = x + dx, y + dy
    direction = DIRECTION_DICT[dx, dy]
    # print("dx: {}, dy: {}, direction: {}".format(dx, dy, direction), file=sys.stderr)

    print(direction)
