#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def search_video_list():
    url = 'https://online.anidub.com/index.php?do=search'

    data = {
        'do': 'search',
        'subaction': 'search',
        'search_start': '1',
        'full_search': '0',
        'result_from': '1',
        'story': 'Моя геройская академия',
    }

    import requests
    rs = requests.post(url, data)

    from bs4 import BeautifulSoup
    root = BeautifulSoup(rs.content, 'html.parser')

    return [a.text.strip() for a in root.select('.newstitle a')]


if __name__ == '__main__':
    items = search_video_list()
    print('Items ({}): {}'.format(len(items), items))

    import json
    json.dump(items, open('video_list.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
