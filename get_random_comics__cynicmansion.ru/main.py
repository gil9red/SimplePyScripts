#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def get_random_comics_url() -> str:
    url = 'https://cynicmansion.ru/'

    import requests
    rs = requests.get(url)

    from bs4 import BeautifulSoup
    root = BeautifulSoup(rs.content, 'lxml')
    comics_number = int(root.select_one('.comics_wrap > table > tr > td > a')['href'].replace('/', ''))

    import random
    random_comics_number = random.randint(1, comics_number)

    return 'https://cynicmansion.ru/{}/'.format(random_comics_number)


def get_comics_image_url(url_comics: str) -> str:
    import requests
    rs = requests.get(url_comics)

    from bs4 import BeautifulSoup
    root = BeautifulSoup(rs.content, 'lxml')

    from urllib.parse import urljoin
    url = urljoin(rs.url, root.select_one('.comics_image > img')['src'])

    return url


def get_random_comics_image_url() -> str:
    url = get_random_comics_url()

    return get_comics_image_url(url)


if __name__ == '__main__':
    url_comics = get_random_comics_url()
    print(url_comics)

    url_image = get_comics_image_url(url_comics)
    print(url_image)

    comics_id = url_comics.split('/')[-2]
    import requests
    rs = requests.get(url_image)

    with open('{}.png'.format(comics_id), 'wb') as f:
        f.write(rs.content)

    print()
    print('Random comics:')
    print(get_random_comics_image_url())
    print(get_random_comics_image_url())
    print(get_random_comics_image_url())
