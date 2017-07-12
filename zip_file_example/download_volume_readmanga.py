#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""Скрипт для скачивания главы по указанному url."""


def get_url_images(url):
    print('Start get_url_images with url:', url)

    import requests
    rs = requests.get(url)

    pattern = '\.init\(.*(\[\[.+\]\]).*\)'

    import re
    match = re.search(pattern, rs.text)
    if match:
        match = match.group(1)
        print('Match:', match)

        # NOTE: если погуглить у меня примеры то можно найти более лучшие чем eval: через json или ast
        urls = eval(match)
        print('After eval:', urls)

        return [i[1] + i[0] + i[2] for i in urls]

    raise Exception('Не получилось из страницы вытащить список картинок главы. '
                    'Используемое регулярное выражение: ', pattern)


def save_urls_to_zip(zip_file_name, urls):
    if not urls:
        print('Cписок изображений пустой.')
        return

    # Создаем архив, у которого именем будет номер главы
    import zipfile
    with zipfile.ZipFile(zip_file_name, mode='w', compression=zipfile.ZIP_DEFLATED) as f:
        import os
        from urllib.request import urlretrieve

        for img_url in urls:
            # Вытаскиваем имя файла
            file_name = os.path.basename(img_url)

            # Имя файла будет {номер_главы}_{номер_страницы}.png
            print(img_url, file_name)

            # Скачиваем файл
            urlretrieve(img_url, file_name)

            # Помещаем в архив
            f.write(file_name)

            # Удаляем файл
            os.remove(file_name)


if __name__ == '__main__':
    url = 'http://readmanga.me/one__piece/vol60/591'

    try:
        urls = get_url_images(url)
        print('Urls:', urls)
        print('Images:', len(urls))

        import os
        file_name = os.path.basename(url) + '.zip'
        save_urls_to_zip(file_name, urls)
        print('Save to filename:', file_name)

    except Exception as e:
        import traceback
        print('Error: {}\n\n{}'.format(e, traceback.format_exc()))
