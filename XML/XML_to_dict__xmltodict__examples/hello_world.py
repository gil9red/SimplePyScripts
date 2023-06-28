#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/martinblech/xmltodict


import json

# pip install xmltodict
import xmltodict


doc = xmltodict.parse(
    """
<mydocument has="an attribute">
    <and>
        <many>elements</many>
        <many>more elements</many>
    </and>
    <plus a="complex">element as well</plus>
</mydocument>
"""
)

print(doc["mydocument"]["@has"])  # an attribute
print(doc["mydocument"]["and"]["many"])  # ['elements', 'more elements']
print(
    doc["mydocument"]["plus"]
)  # OrderedDict([('@a', 'complex'), ('#text', 'element as well')])
print(doc["mydocument"]["plus"]["@a"])  # complex
print(doc["mydocument"]["plus"]["#text"])  # element as well
print()

print(json.dumps(doc, indent=4))
# {
#     "mydocument": {
#         "@has": "an attribute",
#         "and": {
#             "many": [
#                 "elements",
#                 "more elements"
#             ]
#         },
#         "plus": {
#             "@a": "complex",
#             "#text": "element as well"
#         }
#     }
# }
