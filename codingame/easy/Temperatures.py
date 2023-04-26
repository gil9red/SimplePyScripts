#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

n = int(input())  # the number of temperatures to analyse
temps = input()  # the n temperatures expressed as integers ranging from -273 to 5526

temps = [int(i) for i in temps.strip().split()]
print("temps:", temps, file=sys.stderr)

# Проверка того, что 0 уже есть в списке или список температор пустой
if 0 in temps or not temps:
    print(0)
else:
    result = temps[0]

    for i in temps[1:]:
        if i < 0 and result < 0:
            if i > result:
                result = i

        elif i > 0 and result > 0:
            if i < result:
                result = i

        else:
            if abs(i) < result:
                result = i
            elif abs(i) == abs(result):
                result = abs(i)

    print(result)
