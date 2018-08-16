#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from bs4 import BeautifulSoup
import base64


def get_cover_page_image(file_name: str) -> (bytes, str):
    with open(file_name, encoding='utf-8') as f:
        root = BeautifulSoup(f, 'html.parser')

    cover_page_image = root.select_one('coverpage > image')

    # Вытаскиваем значение атрибута href. Эти трудности с генератором из-за возможного пространства
    # имен: l:href, xlink:href
    id_image = next(value for attr, value in cover_page_image.attrs.items() if 'href' in attr)

    # Получится, например, такой css-селектор: binary#cover.jpg
    binary = root.select_one('binary' + id_image)

    # image/jpeg -> jpeg
    content_type = binary.attrs['content-type'].split('/')[-1]

    # Содержимое тега будет извлечено и представлено в виде байтов
    data = binary.text.encode('utf-8')

    return base64.b64decode(data), {'jpeg': 'jpg', 'png': 'png'}[content_type]


if __name__ == '__main__':
    import glob
    import os

    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for fb2_file_name in glob.glob('input/*.fb2'):
        img_data, fmt = get_cover_page_image(fb2_file_name)

        file_name = os.path.basename(fb2_file_name) + '.' + fmt
        file_name = os.path.join(output_dir, file_name)

        with open(file_name, 'wb') as f:
            f.write(img_data)
