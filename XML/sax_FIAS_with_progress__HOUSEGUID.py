#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import xml.sax
from tqdm import trange


# В файле значения HOUSEGUID дублируются
all_house_guid = set()


class AttrHandler(xml.sax.handler.ContentHandler):
    def startElement(self, name, attrs):
        if 'HOUSEGUID' in attrs:
            all_house_guid.add(attrs['HOUSEGUID'])


print('Сбор HOUSEGUID')

parser = xml.sax.make_parser()
parser.setContentHandler(AttrHandler())
parser.parse('AS_HOUSE_20210318_88f2df80-430a-400f-9373-da5b2c80e051.XML')

print(f'Найдено {len(all_house_guid)}')

# Для удобства работы преобразуем в список
all_house_guid = list(all_house_guid)

print('Сохранение в JSON...')

with open('all_house_guid.json', 'w') as f:
    f.write('[')

    for i in trange(len(all_house_guid)):
        if i > 0:
            f.write(',')
        f.write(f'"{all_house_guid[i]}"')

    f.write(']')
