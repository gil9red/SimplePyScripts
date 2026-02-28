#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import itertools
import time


def loop() -> None:
    for c in itertools.cycle("|/-\\"):
        print(c + "\b", flush=True, end="")

        time.sleep(0.3)


if __name__ == "__main__":
    loop()
