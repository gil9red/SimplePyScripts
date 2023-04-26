#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# game loop
while True:
    max_height = 0
    index = -1

    for i in range(8):
        mountain_h = int(input())  # represents the height of one mountain, from 9 to 0.

        if mountain_h > max_height:
            max_height = mountain_h
            index = i

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    # The number of the mountain to fire on.
    print(index)
