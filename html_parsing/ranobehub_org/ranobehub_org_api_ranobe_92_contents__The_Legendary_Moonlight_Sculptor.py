#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import List

import requests


def get_chapters() -> List[str]:
    rs = requests.get('https://ranobehub.org/api/ranobe/92/contents')
    rs.raise_for_status()

    items = []

    for volume in rs.json()['volumes']:
        for chapter in volume['chapters']:
            items.append(f'{volume["name"]} - {chapter["name"]}')

    return items


if __name__ == '__main__':
    items = get_chapters()

    print(f'Items ({len(items)}):')
    for x in items:
        print(f'    {x}')
