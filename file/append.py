#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# https://docs.python.org/3.4/tutorial/inputoutput.html#reading-and-writing-files
# http://pythonworld.ru/tipy-dannyx-v-python/fajly-rabota-s-fajlami.html


from datetime import datetime


# Открыть файл в режиме добавления записей
with open("foo.txt", mode="a", encoding="utf-8") as f:
    now_time = datetime.now().time().strftime("%H:%M:%S")
    f.write(now_time + "\n")

# Открыть файл в режиме добавления записей
with open("foo.txt", mode="a", encoding="utf-8") as f:
    f.write("!!!" + "\n")
    f.write("!!" + "\n")
    f.write("!" + "\n")
