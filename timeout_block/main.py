#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def timeout(seconds=None):
    def wrapper(function_to_decorate):
        def the_wrapper_around_the_original_function(*args, **kwargs):
            from kthread import KThread
            thread = KThread(target=lambda: function_to_decorate(*args, **kwargs))
            thread.start()
            thread.join(timeout=seconds)

            if thread.is_alive():
                thread.kill()

        return the_wrapper_around_the_original_function

    return wrapper


@timeout(seconds=3)
def unlimited_wait():
    import time

    i = 0

    while True:
        i += 1
        print(i)
        time.sleep(1)


if __name__ == '__main__':
    unlimited_wait()
