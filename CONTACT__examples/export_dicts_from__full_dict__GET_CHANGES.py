#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def get_bytes_from_base64_zlib(text_or_tag_or_bytes) -> bytes:
    """
    Декодирует данные из текста или элемента XML из формата BASE64, после разжимает их алгоритмом zlib,
    парсит и возвращает как объект XML.

    """

    if not isinstance(text_or_tag_or_bytes, str) and not isinstance(text_or_tag_or_bytes, bytes):
        text = text_or_tag_or_bytes.text
    else:
        text = text_or_tag_or_bytes

    import base64
    compress_data = base64.b64decode(text)

    import zlib
    return zlib.decompress(compress_data)


if __name__ == '__main__':
    file_name_full_dict = 'mini_full_dict__CONTACT.xml'
    export_dir = 'mini_full_dict__CONTACT'

    import os
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)

    # Parsing
    from bs4 import BeautifulSoup
    root = BeautifulSoup(open(file_name_full_dict, 'rb'), 'lxml')
    # print(root)

    response = root.select_one('response')

    # Если ошибка
    if response['re'] != '0':
        print('Error text: "{}"'.format(response['err_text']))
        quit()

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
