#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import xml.etree.ElementTree as ET


items = [
    {"first_name": "Ivan", "last_name": "Ivanov", "city": "Moscow"},
    {"first_name": "Sergey", "last_name": "Sidorov", "city": "Sochi"},
]

root = ET.Element("root")

for i, item in enumerate(items, 1):
    person = ET.SubElement(root, f"person{i}")

    for k, v in item.items():
        ET.SubElement(person, k).text = v

tree = ET.ElementTree(root)
tree.write("person.xml")
# <root>
#     <person1>
#         <first_name>Ivan</first_name>
#         <last_name>Ivanov</last_name>
#         <city>Moscow</city>
#     </person1>
#     <person2>
#         <first_name>Sergey</first_name>
#         <last_name>Sidorov</last_name>
#         <city>Sochi</city>
#     </person2>
# </root>
