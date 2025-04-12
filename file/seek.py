#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


with open("input__seek.txt", encoding="utf-8") as f:
    for i in range(3):
        print(f"{i}.")

        for line in f:
            print(line.strip(), end=" ")

        print("\n")
        f.seek(0)
