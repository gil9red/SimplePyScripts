#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def get_random_comics_url():
    url = 'https://cynicmansion.ru/'

    import requests
    rs = requests.get(url)

    from bs4 import BeautifulSoup
    root = BeautifulSoup(rs.content, 'lxml')
    comics_number = int(root.select_one('.comics_wrap > table > tr > td > a')['href'].replace('/', ''))

    import random
    random_comics_number = random.randint(1, comics_number)

    return 'https://cynicmansion.ru/{}/'.format(random_comics_number)


if __name__ == '__main__':
    url = get_random_comics_url()
    print(url)

    comics_id = url.split('/')[-2]
    import requests
    rs = requests.get(url)

    with open('{}.png'.format(comics_id), 'wb') as f:
        f.write(rs.content)
