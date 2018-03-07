#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import atexit
import time

start_time = time.clock()


def exit_handler():
    print('Execution time: {:.3f} secs.'.format(time.clock() - start_time))


atexit.register(exit_handler)

number = int(input('Input number: '))
print('My super sum:', sum(range(number ** 2)))
