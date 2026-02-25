#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time


def timer(f):
    def wrapper(*args, **kwargs):
        t = time.time()
        r = f(*args, **kwargs)
        print("Время выполнения функции: %f сек." % (time.time() - t))
        return r

    return wrapper


if __name__ == "__main__":
    @timer
    def my_sleep() -> None:
        print(123)
        time.sleep(0.3)
        print(456)

    my_sleep()

    print()

    @timer
    def my_foo():
        return [i for i in range(10**7) if i % 2 == 0]

    print(my_foo()[:20])
