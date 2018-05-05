#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from urllib.request import urlopen


urls = [
    'http://www.python.org',
    'http://www.python.org/about/',
    'http://www.python.org/doc/',
    'http://www.python.org/download/',
]

from multiprocessing.dummy import Pool as ThreadPool
pool = ThreadPool()
result = pool.map(urlopen, urls)
print(result)
