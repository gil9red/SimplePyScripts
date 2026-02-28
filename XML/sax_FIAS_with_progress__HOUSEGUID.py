#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import xml.sax
from tqdm import tqdm


# В файле значения HOUSEGUID дублируются
all_house_guid = set()


class AttrHandler(xml.sax.handler.ContentHandler):
    def startDocument(self) -> None:
        self.it = iter(tqdm(iter(lambda: 0, 1)))

    def startElement(self, name, attrs) -> None:
        if "HOUSEGUID" in attrs:
            all_house_guid.add(attrs["HOUSEGUID"])

        next(self.it)


print("Сбор HOUSEGUID")

parser = xml.sax.make_parser()
parser.setContentHandler(AttrHandler())
parser.parse("AS_HOUSE_20210318_88f2df80-430a-400f-9373-da5b2c80e051.XML")

print(f"Найдено {len(all_house_guid)}")

print("Сохранение в JSON...")

with open("all_house_guid.json", "w") as f:
    f.write("[")

    for i, guid in tqdm(enumerate(all_house_guid), total=len(all_house_guid)):
        if i > 0:
            f.write(",")
        f.write(f'"{guid}"')

    f.write("]")
