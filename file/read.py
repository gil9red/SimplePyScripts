#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# https://docs.python.org/3.4/tutorial/inputoutput.html#reading-and-writing-files
# http://pythonworld.ru/tipy-dannyx-v-python/fajly-rabota-s-fajlami.html


# Открыть файл в режиме чтения
with open("foo.txt", mode="r", encoding="utf-8") as f:
    print(f.read())

print()

# Открыть файл в режиме чтения и построчно считать файл
with open("foo.txt", mode="r", encoding="utf-8") as f:
    for line in f:
        print(line, end="")
