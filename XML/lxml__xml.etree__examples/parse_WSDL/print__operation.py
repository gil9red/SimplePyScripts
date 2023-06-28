#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from lxml import etree


root = etree.parse(open("smev-message-exchange-service-1.3.wsdl", "rb"))

for operation_node in root.xpath(
    '//*[local-name()="portType"]/*[local-name()="operation"]'
):
    print(operation_node.attrib["name"])

    text = operation_node.xpath('./*[local-name()="documentation"]/text()')[0]
    text = " ".join(filter(None, map(str.strip, text.split("\n"))))
    print(f'    "{text}"')
    print()
