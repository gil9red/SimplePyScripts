#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


items = [
    {"first_name": "Ivan", "last_name": "Ivanov", "city": "Moscow"},
    {"first_name": "Sergey", "last_name": "Sidorov", "city": "Sochi"},
]


import xml.etree.ElementTree as ET
root = ET.Element('root')

for i, item in enumerate(items, 1):
    person = ET.SubElement(root, 'person' + str(i))
    ET.SubElement(person, 'first_name').text = item['first_name']
    ET.SubElement(person, 'last_name').text = item['last_name']
    ET.SubElement(person, 'city').text = item['city']

tree = ET.ElementTree(root)
tree.write('xmlf.xml')
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
