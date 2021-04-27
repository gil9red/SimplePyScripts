#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import base64
import zlib
import sys

from typing import Union

from bs4 import BeautifulSoup, Tag


def get_bytes_from_base64_zlib(text_or_tag_or_bytes: Union[str, bytes, Tag]) -> bytes:
    """
    Декодирует данные из текста или элемента XML из формата BASE64, после разжимает их алгоритмом zlib,
    парсит и возвращает как объект XML.

    """

    if not isinstance(text_or_tag_or_bytes, str) and not isinstance(text_or_tag_or_bytes, bytes):
        text = text_or_tag_or_bytes.text
    else:
        text = text_or_tag_or_bytes

    compress_data = base64.b64decode(text)
    return zlib.decompress(compress_data)


if __name__ == '__main__':
    file_name_full_dict = 'mini_full_dict__CONTACT.xml'
    export_dir = 'mini_full_dict__CONTACT'

    import os
    os.makedirs(export_dir, exist_ok=True)

    # Parsing
    root = BeautifulSoup(open(file_name_full_dict, 'rb'), 'lxml')
    response = root.select_one('response')

    # Если ошибка
    if response['re'] != '0':
        print('Error text: "{}"'.format(response['err_text']))
        sys.exit()

    print('Справочник полный?:', response['full'] == '1')
    print('Версия справочника:', response['version'])
    print()

    for child in response.children:
        # Названия справочников
        if child.name is None:
            continue

        file_name = os.path.join(export_dir, child.name) + '.xml'
        print(file_name)

        with open(file_name, 'w', encoding='cp1251') as f:
            data = get_bytes_from_base64_zlib(child)
            f.write(data.decode(encoding='cp1251'))
