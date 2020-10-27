#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from multiprocessing.dummy import Pool as ThreadPool
import time

from bs4 import BeautifulSoup
import requests


def go(url):
    rs = requests.get(url)
    root = BeautifulSoup(rs.content, 'html.parser')
    return root.select_one('.user-details > a').text.strip()


urls = [
    'https://ru.stackoverflow.com/questions/962400', 'https://ru.stackoverflow.com/questions/962311',
    'https://ru.stackoverflow.com/questions/962128', 'https://ru.stackoverflow.com/questions/962396',
    'https://ru.stackoverflow.com/questions/962349'
]

t = time.time()
result = [go(url) for url in urls]
print(result)
print('Elapsed {:.3f} secs'.format(time.time() - t))
# ['Streletz', 'Kromster', 'Stepan Kasyanenko', 'Kromster', 'JamesJGoodwin']
# Elapsed 6.030 secs

print()

t = time.time()
pool = ThreadPool()
result = pool.map(go, urls)
print(result)
print('Elapsed {:.3f} secs'.format(time.time() - t))
# ['Streletz', 'Kromster', 'Stepan Kasyanenko', 'Kromster', 'JamesJGoodwin']
# Elapsed 3.203 secs
