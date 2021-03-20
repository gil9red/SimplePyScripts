#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import xml.sax
from tqdm import tqdm


f = open('all_house_guid.json', 'w')
f.write('[')


class AttrHandler(xml.sax.handler.ContentHandler):
    def startDocument(self):
        self.it = iter(tqdm(iter(lambda: 0, 1)))
        self.number = 0

    def startElement(self, name, attrs):
        if 'HOUSEGUID' in attrs:
            guid = attrs['HOUSEGUID']
            if self.number > 0:
                f.write(',')
            f.write(f'"{guid}"')

            self.number += 1

        next(self.it)


print('Сбор HOUSEGUID и сохранение в JSON')

parser = xml.sax.make_parser()
parser.setContentHandler(AttrHandler())
parser.parse('AS_HOUSE_20210318_88f2df80-430a-400f-9373-da5b2c80e051.XML')

f.write(']')
f.close()
