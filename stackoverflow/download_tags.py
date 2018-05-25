#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Download tags with description and save in file as JSON.

"""


import requests
from bs4 import BeautifulSoup
import time
import itertools


def get_all_tags(need_pages=None, on_exception_stop=False) -> dict:
    """
    Функция парсит страницу тегов/меток и возвращает их.

    :param need_pages: Т.к. теги будут в порядке убывания популярности, то теги на первых десятках страниц будут
    гарантировано заполнены, из-за их популярности, остальные может не иметь смысла скачивать
    Пример получения первых 20 страниц: NEED_PAGES = 20
    :param on_exception_stop: если True и при парсинге возникнет исключение, парсер будет остановлен
    :return: dict
    """

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }

    tags = dict()

    for page in itertools.count(start=1):
        print('page:', page)

        try:
            rs = requests.get('http://ru.stackoverflow.com/tags?page={}&tab=popular'.format(page), headers=headers)
            root = BeautifulSoup(rs.content, 'html.parser')

            for tag in [a.text.strip() for a in root.select('.tag-cell > a')]:
                print('  tag: "{}"'.format(tag))

                url_info = 'http://ru.stackoverflow.com/tags/{}/info'.format(tag)

                rs = requests.get(url_info, headers=headers)
                root = BeautifulSoup(rs.content, 'html.parser')

                # TODO: Ignore tags without description
                if root.select_one('.post-text'):
                    tags[tag] = {
                        'url_info': url_info,

                        # TODO: scrap only need text
                        'description': root.select_one('.post-text').text.strip(),
                    }

                time.sleep(2)

        except Exception as e:
            import traceback
            print("ERROR: {}\n\n{}".format(e, traceback.format_exc()))

            if on_exception_stop:
                break

        print()

        if page == need_pages:
            break

    return tags


if __name__ == '__main__':
    # # Parse all pages:
    # tags = get_all_tags()
    tags = get_all_tags(need_pages=10)

    import json
    json.dump(tags, open('tags.json', 'w', encoding='utf-8'), ensure_ascii=False)
