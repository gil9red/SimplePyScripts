#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import List


def get_shorted_name(name: str) -> str:
    """
    in = 'Богиня благословляет этот прекрасный мир / Kono Subarashii Sekai ni Shukufuku wo OVA-2'
    out = 'Богиня благословляет этот прекрасный мир OVA-2'

    in = 'Моя геройская академия ТВ-2 / Boku no Hero Academia TV-2 [25 из 25]'
    out = 'Моя геройская академия ТВ-2 [25 из 25]'

    """

    import re

    if '[' in name or 'OVA' in name:
        first, last = map(str.strip, name.split('/'))

        match = re.search('(\[.+?\])|(OVA.*)', last)
        if match and not first.endswith(match.group(0)):
            first += ' ' + match.group(0)

        return first

    return name


def search_video_list(text, short_name=True) -> List[str]:
    url = 'https://online.anidub.com/index.php?do=search'

    data = {
        'do': 'search',
        'subaction': 'search',
        'search_start': '1',
        'full_search': '0',
        'result_from': '1',
        'story': text,
    }

    # NOTE: tor должен быть запущен
    # pip install -U requests[socks]
    import requests
    proxies = {
        'http': 'socks5://localhost:9050',
        'https': 'socks5://localhost:9050'
    }
    rs = requests.post(url, data, proxies=proxies)

    from bs4 import BeautifulSoup
    root = BeautifulSoup(rs.content, 'html.parser')

    items = []

    for a in root.select('.newstitle a'):
        name = a.text.strip()

        if short_name:
            name = get_shorted_name(name)

        items.append(name)

    return items


if __name__ == '__main__':
    text = 'Моя геройская академия'

    items = search_video_list(text, short_name=False)
    print('Items ({}): {}'.format(len(items), items))

    items = search_video_list(text)
    print('Items ({}): {}'.format(len(items), items))

    import json
    json.dump(items, open('video_list.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=4)

    # items = search_video_list('Богиня благословляет этот прекрасный мир')
    # print('Items ({}): {}'.format(len(items), items))
