#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""Скрипт для скачивания главы по указанному url."""


import re
import os
from urllib.parse import urljoin
from urllib.request import urlretrieve
from zipfile import ZipFile
import traceback

import requests


def get_url_images(url):
    print('Start get_url_images with url:', url)

    rs = requests.get(url)

    re_expr = '\.init\(.*(\[\[.+\]\]).*\)'
    match = re.search(re_expr, rs.text)
    if match:
        match = match.group(1)
        print('Match:', match)

        urls = eval(match)
        print('After eval:', urls)

        return [urljoin(i[1], i[0] + i[2]) for i in urls]

    raise Exception('Не получилось из страницы вытащить список картинок главы. '
                    'Используемое регулярное выражение: ', re_expr)


if __name__ == '__main__':
    url = 'http://readmanga.me/one__piece/vol60/591'

    try:
        url = 'http://readmanga.me/one__piece/vol60/591'
        urls = get_url_images(url)
        print('Urls:', urls)

        # Если список изображений не пустой
        if urls:
            print('Всего картинок:', len(urls))

            # Создаем архив, у которого именем будет номер главы
            with ZipFile(os.path.basename(url) + '.zip', mode='w') as myzip:
                for img_url in urls:
                    # Вытаскиваем имя файла
                    file_name = os.path.basename(img_url)

                    # Имя файла будет {номер_главы}_{номер_страницы}.png
                    print(img_url, file_name)

                    # Скачиваем файл
                    urlretrieve(img_url, file_name)

                    # Помещаем в архив
                    myzip.write(file_name)

                    # Удаляем файл
                    os.remove(file_name)

    except Exception as e:
        print('Error: {}\n\n{}'.format(e, traceback.format_exc()))
