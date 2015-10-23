#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""Скрипт парсит файл формата fb2, вытаскивает из него картинки и сохраняет их в папке с таким же названием,
как файл fb2."""


# <binary id="cover.jpg" content-type="image/jpeg">

import os
import base64

from lxml import etree

fb2_file_name = 'Непутевый ученик в школе магии 1. Зачисление в школу (Часть 1).fb2'


with open(fb2_file_name, encoding='utf8') as fb2:
    tree = etree.XML(fb2.read().encode())

    for binary in tree.xpath("//*[local-name()='binary']"):

        # im = Image.open(StringIO(binary.text))
        content_type = binary.attrib['content-type']

        print('short_content_type =', content_type)

        dir_im = os.path.splitext(fb2_file_name)[0]
        if not os.path.exists(dir_im):
            os.makedirs(dir_im)

        im_id = binary.attrib['id']
        print('id =', im_id)

        if content_type is not None:
            if 'jpeg' in content_type:
                if not im_id.endswith('jpg') and not im_id.endswith('jpeg'):
                    im_id += '.' + content_type

            elif not im_id.endswith(content_type):
                im_id += '.' + content_type

        print(im_id)
        im_file_name = os.path.join(dir_im, im_id)
        print(im_file_name)
        with open(im_file_name, mode='wb') as f:
            im_data = base64.b64decode(binary.text.encode())
            f.write(im_data)

        print()

# xml = '''<?xml version="1.0" encoding="UTF-8"?>
# <soft>
#     <os>
#         <item name="linux" dist="ubuntu">
#             This text about linux
#         </item>
#         <item name="mac os">
#             Apple company
#         </item>
#         <item name="windows" dist="XP" />
#     </os>
# </soft>'''
#
# from lxml import etree
#
# tree = etree.XML(xml.encode()) # Парсинг строки
# print(tree)
# print(tree.getroot().items())
# print(dir(tree))
#
# #tree = etree.parse('1.xml') # Парсинг файла
#
# nodes = tree.xpath('//item') # Открываем раздел
# for node in nodes: # Перебираем элементы
#     print(node.tag,node.keys(),node.values())
#     print('name =',node.get('name')) # Выводим параметр name
#     print('text =',[node.text]) # Выводим текст элемента
#
# # # Доступ к тексту напрямую, с указанием фильтра
# # print( 'text1',tree.xpath('/soft/os/item[@name="linux"]/text()'))
# # print( 'text2',tree.xpath('/soft/os/item[2]/text()'))
# # # Доступ к параметру напрямую
# # print( 'dist',tree.xpath('/soft/os/item[@name="linux"]')[0].get('dist'))
# # # Выборка по ключу
# # print( 'dist by key',tree.xpath('//*[@name="windows"]')[0].get('dist'))
# #
# # print( 'iterfind:')
# # for node in tree.iterfind('.//item'): # поиск элементов
# #     print( node.get('name'))
# #
# # # Рекурсивный перебор элементов
# # print( 'recursiely:')
# # def getn(node):
# #     print( node.tag,node.keys())
# #     for n in node:
# #         getn(n)
# getn(tree.getroottree().getroot())