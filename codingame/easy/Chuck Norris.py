#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

message = input()
print(message, file=sys.stderr)

# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)


def Chuck_Norris_encode(text):
    last_c = text[0]
    count = 1

    result = "00 " if last_c == "0" else "0 "

    for i in range(len(text))[1:]:
        c = text[i]

        if c != last_c:
            result += "0" * count + " "
            count = 1
            result += "00 " if c == "0" else "0 "
        else:
            count += 1

        last_c = c

    result += "0" * count

    return result


if __name__ == '__main__':
    # Бинарная строка должна содержать 7 символов, а bin в может вернуть
    # строку меньшего размера, убрав ненужные нули
    text = "".join([bin(ord(c))[2:].rjust(7, "0") for c in message])
    print(Chuck_Norris_encode(text))
