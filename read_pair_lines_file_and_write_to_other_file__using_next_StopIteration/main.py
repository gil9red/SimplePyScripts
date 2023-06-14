#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


with (
    open("short_100.txt", encoding="utf-8") as in_f,
    open("long_100.txt", "w", encoding="utf-8") as out_f,
):
    while True:
        try:
            line = f"{next(in_f).rstrip()} {next(in_f).rstrip()}\n"
            out_f.write(line)
        except StopIteration:
            break
