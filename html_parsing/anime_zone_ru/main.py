#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import re
import zipfile
import os.path

from urllib.parse import urljoin
from pathlib import Path

import requests
from bs4 import BeautifulSoup


DIR = Path(__file__).resolve().parent

session = requests.Session()
session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'

re_no_digits = re.compile(r'\D')


def download(url: str, directory=DIR) -> str:
    rs = session.get(url)
    root = BeautifulSoup(rs.content, 'html.parser')

    chapter = root.select_one('select[name=chapter] > option[selected]').get_text(strip=True)
    chapter = chapter + '.zip'
    file_name = directory / chapter

    with zipfile.ZipFile(file_name, mode='w', compression=zipfile.ZIP_DEFLATED) as f:
        for a in root.select('a.gallery[href]'):
            img_url = urljoin(rs.url, a['href'])
            img_text = a.get_text(strip=True)

            # "[001]" -> "001"
            img_text = re_no_digits.sub('', img_text)

            _, ext = os.path.splitext(img_url)
            img_file_name = img_text + ext

            f.writestr(
                img_file_name,
                session.get(img_url).content,
            )

    return file_name


if __name__ == '__main__':
    url = 'http://anime-zone.ru/manga/chapter/naruto/07/055/'
    print(download(url))

    url = 'http://anime-zone.ru/manga/chapter/naruto/17/150/'
    print(download(url))
