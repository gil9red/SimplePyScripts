#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def search_video_list(text) -> list:
    url = 'https://online.anidub.com/index.php?do=search'

    data = {
        'do': 'search',
        'subaction': 'search',
        'search_start': '1',
        'full_search': '0',
        'result_from': '1',
        'story': text,
    }

    import requests
    rs = requests.post(url, data)

    from bs4 import BeautifulSoup
    root = BeautifulSoup(rs.content, 'html.parser')

    return [a.text.strip() for a in root.select('.newstitle a')]


def get_shorted_names(items: list) -> list:
    """
    in = ['Богиня благословляет этот прекрасный мир / Kono Subarashii Sekai ni Shukufuku wo OVA-2', 'Богиня благословляет этот прекрасный мир ТВ-2 / Kono Subarashii Sekai ni Shukufuku wo TV-2 [10 из 10]', 'Богиня благословляет этот прекрасный мир OVA / Kono Subarashii Sekai ni Shukufuku wo! OVA', 'Богиня благословляет этот прекрасный мир / Kono Subarashii Sekai ni Shukufuku wo! [10 из 10]']
    out = ['Богиня благословляет этот прекрасный мир OVA-2', 'Богиня благословляет этот прекрасный мир ТВ-2 [10 из 10]', 'Богиня благословляет этот прекрасный мир OVA', 'Богиня благословляет этот прекрасный мир [10 из 10]']

    in = ['Моя геройская академия ТВ-2 / Boku no Hero Academia TV-2 [25 из 25]', 'Моя геройская академия / Boku no Hero Academia [13 из 13]']
    out = ['Моя геройская академия ТВ-2 [25 из 25]', 'Моя геройская академия [13 из 13]']

    """

    new_items = []

    import re

    for name in items:
        first, last = map(str.strip, name.split('/'))

        match = re.search('(\[.+?\])|(OVA.*)', last)
        if match and not first.endswith(match.group(0)):
            first += ' ' + match.group(0)

        new_items.append(first)

    return new_items


if __name__ == '__main__':
    items = search_video_list('Моя геройская академия')
    print('Items ({}): {}'.format(len(items), items))

    items = get_shorted_names(items)
    print('Items ({}): {}'.format(len(items), items))

    import json
    json.dump(items, open('video_list.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=4)

    # items = search_video_list('Богиня благословляет этот прекрасный мир')
    # print('Items ({}): {}'.format(len(items), items))
