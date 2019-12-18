#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Вытаскивание и сохранение на диск файлов логотипов

"""


if __name__ == '__main__':
    FILE_NAME_DICT_LOGO = 'mini_full_dict__CONTACT/logo.xml'
    DIR_LOGO_IMAGES = 'logo_images'

    import os
    os.makedirs(DIR_LOGO_IMAGES, exist_ok=True)

    from bs4 import BeautifulSoup
    root = BeautifulSoup(open(FILE_NAME_DICT_LOGO, 'rb'), 'lxml')

    for row in root.select('rowdata > row'):
        logo_name = row['logo_name']
        print(logo_name)

        logo_data = row['logo_data']
        import base64
        img_data = base64.b64decode(logo_data)

        file_name = os.path.join(DIR_LOGO_IMAGES, logo_name)

        with open(file_name, 'wb') as f:
            f.write(img_data)
