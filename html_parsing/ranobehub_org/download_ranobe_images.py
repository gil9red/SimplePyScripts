#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import re
import time

from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def get_valid_filename(s: str) -> str:
    s = s.strip().replace(':', '.')
    return re.sub(r'(?u)[^-\w. ]', '', s)


DIR = Path(__file__).resolve().parent

session = requests.Session()
session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0'


def parse(start_url: str, download_path: Path = DIR):
    url = start_url

    while True:
        rs = session.get(url)
        soup = BeautifulSoup(rs.content, 'html.parser')

        title = soup.select_one('title').get_text(strip=True)
        print(title)

        img_urls = []
        for img_el in soup.select('img[data-media-id]'):
            media_id = img_el['data-media-id']
            url = urljoin(rs.url, f'/api/media/{media_id}')
            if url not in img_urls:
                img_urls.append(url)

        if img_urls:
            print(f'    Изображений: {len(img_urls)}')

            # Example: 'Да будет благословен этот прекрасный мир! / Том 666 / Веб-новелла: Короткая история богини'
            #       -> ['Да будет благословен этот прекрасный мир', 'Том 666', 'Веб-новелла Короткая история богини']
            parts: list[str] = [get_valid_filename(el) for el in title.split('/')]
            ranobe_title: str = parts[0]
            chapter_title: str = '. '.join(parts[1:])

            dir_ranobe = download_path / ranobe_title
            dir_ranobe.mkdir(parents=True, exist_ok=True)

            for i, url in enumerate(img_urls, 1):
                rs = session.get(url)
                time.sleep(0.1)

                img_path = dir_ranobe / f'{chapter_title}. {i}.png'
                img_path.write_bytes(rs.content)

        next_chapter_link_el = soup.select_one('a[data-next-chapter-link]')
        if not next_chapter_link_el.get('href'):
            break

        url = urljoin(rs.url, next_chapter_link_el['href'])

        time.sleep(1)


if __name__ == '__main__':
    url = 'https://ranobehub.org/ranobe/131/1/1'
    parse(url)
