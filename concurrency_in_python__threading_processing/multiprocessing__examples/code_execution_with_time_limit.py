#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import multiprocessing


def run():
    import time

    i = 1

    # Бесконечный цикл
    while True:
        print(i)
        i += 1

        time.sleep(1)


if __name__ == "__main__":
    p = multiprocessing.Process(target=run)
    p.start()

    # Wait
    p.join(5)

    # Если процесс живой,то убиваем его
    if p.is_alive():
        print("Kill it.")

        # Terminate
        p.terminate()
