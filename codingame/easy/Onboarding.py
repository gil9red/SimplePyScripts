#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# game loop
while True:
    enemy_1 = input()  # name of enemy 1
    dist_1 = int(input())  # distance to enemy 1
    enemy_2 = input()  # name of enemy 2
    dist_2 = int(input())  # distance to enemy 2

    # Write an action using print

    # Enter the code here
    if dist_1 < dist_2:
        print(enemy_1)
    else:
        print(enemy_2)
