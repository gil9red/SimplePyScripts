#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


class Object:
    a = 0
    b = '123'

    def __init__(self):
        self.c = 3
        self.items = [1, 2, 3, 4]


def object_to_dict(object):
    fields_from_class = dict(filter(lambda x: not x[0].startswith('_'), object.__class__.__dict__.items()))
    fields_from_object = dict(filter(lambda x: not x[0].startswith('_'), object.__dict__.items()))

    fields = dict()
    fields.update(fields_from_class)
    fields.update(fields_from_object)

    return fields

obj = Object()
fields = object_to_dict(obj)
print(fields)
print()

import json
print(json.dumps(fields, ensure_ascii=False, indent=4))
