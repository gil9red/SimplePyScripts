#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# Скрипт качает главу по адресу


from grab import Grab
import re
import requests
from zipfile import ZipFile
import os


def download_file(url, file_name):
    # Попытаемся скачать аудиозапись
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        # Создаем файл и в него записываем файл с сервера
        with open(file_name, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
    else:
        raise Exception('Ошибка при скачивании "{}": {} - {}'.format(url, r.status_code, r.reason))


if __name__ == '__main__':
    url = 'http://readmanga.me/one__piece/vol60/591'

    g = Grab()
    g.go(url)

    # Список картинок описан в переменной pictures
    # Выковыриваем инициализацию переменной
    m = re.search(r'var pictures = (.+?);', g.response.body)
    url_images_str = m.group(1)

    # Выковыриваем ссылки на изображения
    url_images = re.findall(r'https?.+?png', url_images_str)
    print('Всего изображений:', len(url_images))

    # Если список изображений не пустой
    if url_images:
        # Создаем архив, у которого именем будет номер главы
        with ZipFile(os.path.basename(url) + '.zip', mode='w') as myzip:
            for im in url_images:
                # Вытаскиваем имя файла
                file_name = os.path.basename(im)

                # Имя файла будет {номер_главы}_{номер_страницы}.png
                # Нам же нужен только {номер_страницы}.png его и вытаскиваем
                file_name = file_name.split('_')[-1]
                print(im, file_name)

                # Скачиваем файл
                download_file(im, file_name)

                # Помещаем в архив
                myzip.write(file_name)

                # Удаляем файл
                os.remove(file_name)
