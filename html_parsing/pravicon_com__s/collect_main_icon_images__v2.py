#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import re
import shutil

from config import DIR_DUMP


DIR_DUMP_IMAGES = DIR_DUMP.parent / 'DUMP_images__v2'
DIR_DUMP_IMAGES.mkdir(parents=True, exist_ok=True)

pattern = re.compile(r'icon-\d+__(.+)')


for file_name in DIR_DUMP.glob('*/Главное изображение.jpg'):
    m = pattern.search(file_name.parent.stem)
    new_file_name = DIR_DUMP_IMAGES / f'{m.group(1)}.jpg'

    shutil.copy(file_name, new_file_name)
