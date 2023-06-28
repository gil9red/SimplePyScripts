#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/martinblech/xmltodict


import json

# pip install xmltodict
import xmltodict


# The optional argument `postprocessor` is a function that takes `path`, `key` and `value` as positional arguments
# and returns a new `(key, value)` pair where both `key` and `value` may have changed. Usage example:


def postprocessor(path, key, value):
    try:
        return key + ":int", int(value)
    except (ValueError, TypeError):
        return key, value


doc = xmltodict.parse("<a><b>1</b><b>2</b><b>x</b></a>", postprocessor=postprocessor)

print(json.dumps(doc, indent=4))
# {
#     "a": {
#         "b:int": [
#             1,
#             2
#         ],
#         "b": "x"
#     }
# }
