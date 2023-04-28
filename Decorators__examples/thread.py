#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
from threading import Thread


def thread(my_func):
    def wrapper(*args, **kwargs):
        my_thread = Thread(target=my_func, args=args, kwargs=kwargs)
        my_thread.start()

    return wrapper


if __name__ == "__main__":
    @thread
    def _print_and_sleep(timeout=2):
        print("start. print_and_sleep")

        time.sleep(timeout)
        print("finish. print_and_sleep")

    @thread
    def _print_loop(name, max_num=10):
        print("start. _print_loop")

        i = 0

        while True:
            print(name, i)
            time.sleep(1)

            i += 1
            if i == max_num:
                break

        print("finish. _print_loop")

    _print_and_sleep()
    _print_and_sleep(4)
    _print_and_sleep()
    _print_loop("  loop")
