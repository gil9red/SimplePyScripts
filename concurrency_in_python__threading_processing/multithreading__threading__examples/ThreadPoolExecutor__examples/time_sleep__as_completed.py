#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor-example


import concurrent.futures
import time
from random import randint


MAX_WORKERS = 5


def run(name):
    time.sleep(randint(1, 4))
    return f'name: {name}'


executor = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS)

futures = [executor.submit(run, i + 1) for i in range(20)]

for future in concurrent.futures.as_completed(futures):
    print(future.result())
