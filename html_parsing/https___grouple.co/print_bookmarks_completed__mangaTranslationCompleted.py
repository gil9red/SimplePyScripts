#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from bs4 import BeautifulSoup
import requests

from config import LOGIN, PASSWORD


FORM_DATA = {
    'username': LOGIN,
    'password': PASSWORD,
}

session = requests.Session()
session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'

rs = session.post('https://grouple.co/login/authenticate', data=FORM_DATA)
rs.raise_for_status()

rs = session.get('https://grouple.co/private/bookmarks?status=WATCHING')
rs.raise_for_status()

root = BeautifulSoup(rs.content, 'html.parser')
items = []

for row in root.select('.bookmark-row'):
    a = row.select_one('.site-element')

    is_complete = False

    sup = a.select_one('sup')
    if sup:
        is_complete = bool(sup.select_one('.mangaTranslationCompleted'))

        # Удаление сноски ("Выпуск завершен", "переведено" и т.п.), чтобы в title она не попала
        sup.decompose()

    title = a.get_text(strip=True)
    url = a['href']
    items.append(
        (is_complete, title, url)
    )

print(f'Total bookmarks ({len(items)}):')
for _, title, url in items:
    print(f'    {repr(title)}: {url}')

print('\n')

completed = [(title, url) for is_complete, title, url in items if is_complete]
print(f'Total bookmarks completed ({len(completed)}):')
for title, url in completed:
    print(f'    {repr(title)}: {url}')
