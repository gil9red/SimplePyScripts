#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""Скрипт парсит файл формата fb2, вытаскивает из него картинки и сохраняет их в папке с таким же названием,
как файл fb2."""


import os
import base64
import io

from lxml import etree
from PIL import Image


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


if __name__ == '__main__':
    fb2_file_name = 'Непутевый ученик в школе магии 1. Зачисление в школу (Часть 1).fb2'

    dir_im = os.path.splitext(fb2_file_name)[0]
    if not os.path.exists(dir_im):
        os.makedirs(dir_im)
    print(dir_im + ':')

    total_image_size = 0

    with open(fb2_file_name, encoding='utf8') as fb2:
        tree = etree.XML(fb2.read().encode())

        binaries = tree.xpath("//*[local-name()='binary']")
        for i, binary in enumerate(binaries, 1):
            try:
                content_type = binary.attrib['content-type']
                short_content_type = content_type.split('/')[-1]

                im_id = binary.attrib['id']

                if 'jpeg' in short_content_type:
                    if not im_id.endswith('jpg') and not im_id.endswith('jpeg'):
                        im_id += '.' + short_content_type

                elif not im_id.endswith(short_content_type):
                    im_id += '.' + short_content_type

                im_file_name = os.path.join(dir_im, im_id)
                im_data = base64.b64decode(binary.text.encode())
                with open(im_file_name, mode='wb') as f:
                    f.write(im_data)

                im = Image.open(io.BytesIO(im_data))
                count_bytes = len(im_data)
                total_image_size += count_bytes
                print('    {}. {} {} format={} size={}'.format(i, im_id, sizeof_fmt(count_bytes),
                                                               im.format, im.size))

            except Exception as e:
                import traceback
                traceback.print_exc()

    fb2_file_size = os.path.getsize(fb2_file_name)
    print()
    print('fb2 file size =', sizeof_fmt(fb2_file_size))
    print('total image size = {} ({:.2f}%)'.format(sizeof_fmt(total_image_size),
                                                   total_image_size / fb2_file_size * 100))
