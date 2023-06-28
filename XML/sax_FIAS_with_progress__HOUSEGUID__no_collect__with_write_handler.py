#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import xml.sax
from tqdm import tqdm


class WriteHouseGuidHandler(xml.sax.handler.ContentHandler):
    def __init__(self, file_name: str):
        super().__init__()

        self.f = open(file_name, "w")
        self.it = None
        self.number = 0

    def startDocument(self):
        self.it = iter(tqdm(iter(lambda: 0, 1)))
        self.number = 0
        self.f.write("[")

    def startElement(self, name, attrs):
        if "HOUSEGUID" in attrs:
            guid = attrs["HOUSEGUID"]

            if self.number > 0:
                self.f.write(",")
            self.f.write(f'"{guid}"')

            self.number += 1

        next(self.it)

    def endDocument(self):
        self.f.write("]")
        self.f.close()


print("Сбор HOUSEGUID и сохранение в JSON")

parser = xml.sax.make_parser()
parser.setContentHandler(WriteHouseGuidHandler("all_house_guid.json"))
parser.parse("AS_HOUSE_20210318_88f2df80-430a-400f-9373-da5b2c80e051.XML")
