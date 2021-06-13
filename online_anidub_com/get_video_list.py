#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys
import re

from typing import List
from pathlib import Path

from bs4 import BeautifulSoup


ROOT_DIR = Path(__file__).resolve().parent


sys.path.append(str(ROOT_DIR.parent / 'using_proxy'))
import proxy_requests__upgraded
ProxyRequests = proxy_requests__upgraded.ProxyRequests


DEBUG_LOG = False
proxy_requests__upgraded.DEBUG_LOG = DEBUG_LOG


def _get_title(el) -> str:
    title = el.get_text(strip=True)
    return re.sub(r'\s{2,}', ' ', title)


def search_video_list(text: str) -> List[str]:
    url = 'https://online.anidub.com/index.php?do=search'

    data = {
        'do': 'search',
        'subaction': 'search',
        'search_start': '0',
        'full_search': '0',
        'result_from': '1',
        'story': text,
    }
    headers = {
        'Host': 'online.anidub.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Origin': 'https://online.anidub.com',
        'Referer': 'https://online.anidub.com/index.php?do=search',
    }

    while True:
        rq = ProxyRequests(url)
        rs = rq.post(data=data, headers=headers)

        content = rs.content

        if b'Attention Required! | Cloudflare' in content \
                or b'Access denied | online.anidub.com used Cloudflare to restrict access' in content:
            DEBUG_LOG and print('Fail! Cloudflare!')
            continue

        break

    root = BeautifulSoup(content, 'html.parser')
    return [_get_title(a) for a in root.select('.th-title')]


if __name__ == '__main__':
    text = 'Моя геройская академия'

    items = search_video_list(text)
    print(f'Items ({len(items)}):')
    for x in items:
        print(f'    {x}')

    import json
    json.dump(items, open('video_list.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
