#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://ru.stackoverflow.com/q/861914/201445


# pip install xmltodict
import xmltodict


items = [
    {"first_name": "Ivan", "last_name": "Ivanov", "city": "Moscow"},
    {"first_name": "Sergey", "last_name": "Sidorov", "city": "Sochi"},
]
root = dict()

for i, item in enumerate(items, 1):
    root["person" + str(i)] = item

my_dict = {"root": root}
# my_dict = {
#     'root': {
#         'person1': {"first_name": "Ivan", "last_name": "Ivanov", "city": "Moscow"},
#         'person2': {"first_name": "Sergey", "last_name": "Sidorov", "city": "Sochi"},
#     }
# }

# Параметр full_document=False убирает из XML строку "<?xml version="1.0 ..."
print(xmltodict.unparse(my_dict, pretty=True, full_document=False))
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
