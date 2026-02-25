#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time

from urllib.request import urlopen
from multiprocessing.dummy import Pool as ThreadPool


urls = [
    "http://www.python.org",
    "http://www.python.org/about/",
    "http://www.python.org/doc/",
    "http://www.python.org/download/",
    # 'http://www.onlamp.com/pub/a/python/2003/04/17/metaclasses.html',
    # 'http://www.python.org/getit/',
    # 'http://www.python.org/community/',
    # 'https://wiki.python.org/moin/',
    # 'http://planet.python.org/',
    # 'https://wiki.python.org/moin/LocalUserGroups',
    # 'http://www.python.org/psf/',
    # 'http://docs.python.org/devguide/',
    # 'http://www.python.org/community/awards/'
    # etc..
]

t = time.clock()
results = []
for url in urls:
    result = urlopen(url)
    results.append(result)
print(f"Single thread: {time.clock() - t:.3f} seconds")

# ------- VERSUS ------- #


def go(count=1) -> None:
    t = time.clock()
    pool = ThreadPool(count)
    results = pool.map(urlopen, urls)
    # pool.close()
    # pool.join()
    print(f"{count} Pool: {time.clock() - t:.3f} seconds")


# ------- 1 Pool ------- #
go()

# ------- 2 Pool ------- #
go(2)

# ------- 3 Pool ------- #
go(3)

# ------- 4 Pool ------- #
go(4)

# ------- 8 Pool ------- #
go(8)

# ------- 13 Pool ------- #
go(13)

# # Make the Pool of workers
# pool = ThreadPool(4)
#
# # Open the urls in their own threads
# # and return the results
# results = pool.map(urlopen, urls)
#
# # close the pool and wait for the work to finish
# pool.close()
# pool.join()
