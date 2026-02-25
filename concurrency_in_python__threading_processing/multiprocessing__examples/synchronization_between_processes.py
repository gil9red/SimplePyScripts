#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://docs.python.org/3.6/library/multiprocessing.html#synchronization-between-processes


from multiprocessing import Process, Lock
import time


def f(lock, i) -> None:
    with lock:
        print("hello world", i)

        time.sleep(1)


if __name__ == "__main__":
    lock = Lock()

    for num in range(10):
        Process(target=f, args=(lock, num)).start()
