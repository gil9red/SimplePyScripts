#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor-example


import concurrent.futures
import time
from random import randint


MAX_WORKERS = 5


def run(name):
    print(f"name: {name}")
    time.sleep(randint(1, 4))


executor = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS)

for i in range(20):
    executor.submit(run, i + 1)
