#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def get_html_by_url__from_cache(url, cache_dir='cache'):
    import os
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    file_name = os.path.basename(url).replace(':', '_')
    file_name = cache_dir + '/' + file_name + '.html'

    if os.path.exists(file_name):
        with open(file_name, 'rb') as f:
            return f.read()

    with open(file_name, 'wb') as f:
        import requests
        rs = requests.get(url)
        f.write(rs.content)

        return rs.content


url = 'https://ru.wikipedia.org/wiki/Список_серий_«Наруто»_(сезоны_1—3)'
# url = 'https://ru.wikipedia.org/wiki/Список_серий_«Наруто»_(сезоны_4—6)'
# url = 'https://ru.wikipedia.org/wiki/Список_серий_«Наруто»_(сезоны_7—9)'
# url = 'https://ru.wikipedia.org/wiki/Список_серий_«Наруто:_Ураганные_хроники»_(сезоны_1—4)'
html_content = get_html_by_url__from_cache(url)


from bs4 import BeautifulSoup
root = BeautifulSoup(html_content, 'html.parser')

td_list = []

for td in root.select('td'):
    if td.has_attr('id') and td['id'].startswith('ep'):
        td_list.append(td)
        print(td)
