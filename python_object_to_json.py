#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


class SubField:
    def __init__(self):
        self.flag = True


class Field:
    def __init__(self, tag1, tag2, sub_field_flag=True):
        self.tag1 = tag1
        self.tag2 = tag2

        self.sub_field = SubField()
        self.sub_field.flag = sub_field_flag


class Object:
    a = 0
    b = "123"

    def __init__(self):
        self.c = 3
        self.items = [1, 2, 3, 4]
        self.maps = {
            "is": True,
            "not": 0,
        }

        self.field = Field("abc", "tag2")
        self.field_2 = Field(777, False, sub_field_flag=False)


def object_to_dict(object):
    fields = dict()
    fields.update(object.__class__.__dict__)
    fields.update(object.__dict__)

    fields = dict(filter(lambda x: not x[0].startswith("_"), fields.items()))

    new_fields = dict()
    for k, v in fields.items():
        if hasattr(v, "__dict__"):
            v = object_to_dict(v)

        new_fields[k] = v

    return new_fields


if __name__ == "__main__":
    obj = Object()
    fields = object_to_dict(obj)
    print(fields)
    print()

    import json

    print(json.dumps(fields, ensure_ascii=False, indent=4, sort_keys=True))
