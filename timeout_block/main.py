#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
from kthread import KThread


def timeout(seconds=None, raise_timeout=False):
    def wrapper(function_to_decorate):
        def the_wrapper_around_the_original_function(*args, **kwargs):
            thread = KThread(target=lambda: function_to_decorate(*args, **kwargs))
            thread.start()
            thread.join(timeout=seconds)

            if thread.is_alive():
                thread.kill()

                if raise_timeout:
                    raise TimeoutError()

        return the_wrapper_around_the_original_function

    return wrapper


@timeout(seconds=3)
def unlimited_wait() -> None:
    i = 0

    while True:
        i += 1
        print(i)
        time.sleep(1)


@timeout(seconds=3, raise_timeout=True)
def unlimited_wait2() -> None:
    i = 0

    while True:
        i += 1
        print(i)
        time.sleep(1)


if __name__ == "__main__":
    unlimited_wait()

    unlimited_wait2()
