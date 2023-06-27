#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


if __name__ == "__main__":
    import time

    c = 5

    while True:
        print("!!!")
        time.sleep(1)

        c -= 1
        if not c:
            break

    print("Exit. Конец!")
