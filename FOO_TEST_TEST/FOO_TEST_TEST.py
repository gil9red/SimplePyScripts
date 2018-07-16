#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def get_html_by_url__from_cache(url, cache_dir='cache'):
    import os
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    file_name = os.path.basename(url)

    import re
    file_name = re.sub(r'[^\w\d]', '_', file_name)

    file_name = cache_dir + '/' + file_name + '.html'

    if os.path.exists(file_name):
        with open(file_name, 'rb') as f:
            return f.read()

    with open(file_name, 'wb') as f:
        import requests
        rs = requests.get(url)
        f.write(rs.content)

        return rs.content


def get_urls_of_season_1():
    return [
        'https://ru.wikipedia.org/wiki/Список_серий_«Наруто»_(сезоны_1—3)',
        'https://ru.wikipedia.org/wiki/Список_серий_«Наруто»_(сезоны_4—6)',
        'https://ru.wikipedia.org/wiki/Список_серий_«Наруто»_(сезоны_7—9)',
    ]


from bs4 import BeautifulSoup


# url = 'https://ru.wikipedia.org/wiki/Список_серий_«Наруто:_Ураганные_хроники»_(сезоны_1—4)'


ep_chapters_s1 = []


for url in get_urls_of_season_1():
    html_content = get_html_by_url__from_cache(url)

    root = BeautifulSoup(html_content, 'html.parser')

    for td in root.select('td'):
        if td.has_attr('id') and td['id'].startswith('ep'):
            episode = td.text.strip()
            manga_chapters = td.next_sibling.next_sibling.text.strip()

            ep_chapters_s1.append((episode, manga_chapters))


print(len(ep_chapters_s1), ep_chapters_s1)
