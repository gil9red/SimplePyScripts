#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from bs4 import BeautifulSoup
root = BeautifulSoup(open('the_gamer.htm', 'rb'), 'lxml')

description = root.select_one('.manga-description').text.strip()

# Удаление множества подряд идущих пробелов
import re
description = re.sub(r'\s{2,}', ' ', description)
print(description)

# TODO: ссылка для кнопки "начать чтение"
url_first_volume = root.select_one('.read-first > a')['href']

from urllib.parse import urljoin
# TODO: Брать url из запроса
url_first_volume = urljoin('http://readmanga.me', url_first_volume)
print(url_first_volume)

# TODO: нужно использовать <url_first_volume> чтобы зайти на страницу главы и вытащить список глав
root = BeautifulSoup(open('the_gamer_v1_1.htm', 'rb'), 'lxml')

# TODO: Брать url из запроса
chapter_list = [(option.text.strip(), urljoin('http://readmanga.me', option['value'])) for option in root.select('#chapterSelectorSelect > option')]
print(chapter_list)

for name, url in chapter_list:
    print("{}: {}".format(name, url))


def get_url_images_from_volume(html_volume):
    """
    Функция для вытаскивания ссылок на страницы (картинки) главы.

    """

    # Пример данных: rm_h.init( [['auto/09/79','http://e5.postfact.ru/',"/80/1.jpg_res.jpg",690,21869],['auto/09/79','http://e2.postfact.ru/',"/80/2.jpg_res.jpg",690,19560]], 0, false);
    # То, что в квадратных скобках в init можно распарсить как JSON, осталось регуляркой это вытащить
    re_expr = r'init\(.*(\[\[.+\]\]).*\)'

    import re
    match = re.search(re_expr, html_volume)
    if match:
        json_text = match.group(1)

        # Замена одинарных кавычек на двойные
        json_text = json_text.replace("'", '"')
        print(json_text)

        import json
        json_data = json.loads(json_text)
        print(json_data)

        return [urljoin(data_url[1], data_url[0] + data_url[2]) for data_url in json_data]

    raise Exception('Не получилось из страницы вытащить список картинок главы. '
                    'Используемое регулярное выражение: ', re_expr)


# Для получения ссылок на картинки глав:
html = str(root)
url_images = get_url_images_from_volume(html)
print(url_images)


