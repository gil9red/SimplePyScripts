#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor-example


import concurrent.futures
import time


MAX_WORKERS = 5


# Retrieve a single page and report the URL and contents
def run(name):
    print('name:', name)
    time.sleep(2)


executor = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS)

for i in range(20):
    executor.submit(run, i + 1)
