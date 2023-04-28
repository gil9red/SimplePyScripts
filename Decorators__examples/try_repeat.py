#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import random


# http://ru.stackoverflow.com/a/491681/201445


def try_repeat(func):
    def wrapper(*args, **kwargs):
        count = 10

        while count:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print("Error:", e)
                count -= 1

    return wrapper


@try_repeat
def exception_func():
    if random.randint(0, 1):
        raise Exception("!!!")


exception_func()
