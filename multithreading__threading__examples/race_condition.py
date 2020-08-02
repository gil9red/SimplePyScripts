#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from multiprocessing.dummy import Pool as ThreadPool
import threading


number = 0
DATA = {
    'number': 0
}
lock = threading.Lock()


def inc(*args):
    global number

    DATA['number'] += 1
    number += 1


def inc_lock(*args):
    global number

    with lock:
        number += 1
        DATA['number'] += 1


max_number = 1_000_000

# Only one thread -- main
number = DATA['number'] = 0
for _ in range(max_number):
    inc()
print(number, DATA['number'])
# 1000000 1000000

# Many threads
number = DATA['number'] = 0
pool = ThreadPool()
pool.map(inc, range(max_number))
print(number, DATA['number'])
# 819903 459802

# Many threads
number = DATA['number'] = 0
pool = ThreadPool()
pool.map(inc_lock, range(max_number))
print(number, DATA['number'])
# 1000000 1000000
