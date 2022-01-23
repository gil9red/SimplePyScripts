#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import json
import time
from pathlib import Path

from bs4 import BeautifulSoup

from main import get, session


FILE = Path(__file__).resolve()
DIR = FILE.parent
FILE_CACHE = DIR / f'{FILE.stem}.json'

try:
    cache = json.load(open(FILE_CACHE, encoding='utf-8'))
except:
    cache = dict()


URL_PAGE = 'https://cubiq.ru/gametime/page/{page}/'

if __name__ == '__main__':
    page = 1
    while True:
        url = URL_PAGE.format(page=page)
        print(url)

        try:
            rs = session.get(url)
            root = BeautifulSoup(rs.content, 'html.parser')
            for a in root.select('.gridlove-post > .entry-image > a'):
                game = a['title']
                if game in cache:
                    continue

                url = a['href']
                if data := get(url):
                    time_obj = data['Основной сюжет']
                    cache[game] = {
                        'text': time_obj.text,
                        'seconds': time_obj.seconds,
                    }
                    print(f'Saved {game!r}: {time_obj.text}')

                    json.dump(cache, open(FILE_CACHE, 'w', encoding='utf-8'), indent=4, ensure_ascii=False)
                    time.sleep(1)

            next_page = root.select_one('.gridlove-pagination > .next.page-numbers')
            if not next_page:
                break

            page += 1

        except Exception:
            time.sleep(1)
