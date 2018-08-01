#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def go(url):
    from urllib.request import urlopen
    rs = urlopen(url)
    print(url, rs)

    return rs


urls = [
    'http://www.python.org',
    'http://www.python.org/about/',
    'http://www.python.org/doc/',
    'http://www.python.org/download/',
]

from multiprocessing.dummy import Pool as ThreadPool
pool = ThreadPool()
results = pool.map(go, urls)
print(results)
