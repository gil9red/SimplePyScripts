#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import atexit
from timeit import default_timer as timer


start_time = timer()


def exit_handler():
    print("Execution time: {:.3f} secs.".format(timer() - start_time))


atexit.register(exit_handler)


# OR with decorator:
@atexit.register
def exit_handler():
    print("Execution time: {:.3f} secs.".format(timer() - start_time))


number = int(input("Input number: "))
print("My super sum:", sum(range(number**2)))
