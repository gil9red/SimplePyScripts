#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from multiprocessing import Process, current_process
import time


def run():
    print(current_process())

    for i in 'Hello World!':
        print(i)
        time.sleep(0.2)


if __name__ == '__main__':
    p = Process(target=run, daemon=True)
    p.start()

    # Main process NOT WAIT thread
