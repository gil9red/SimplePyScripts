#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/martinblech/xmltodict#roundtripping


# pip install xmltodict
import xmltodict


class Dog:
    def __init__(self, name):
        self.name = name
        self.type = "Animal"
        self.paws = 4
        self.has_tail = True

    def __repr__(self):
        return f'<Dog name={self.name} type="{self.type}" paws="{self.paws}" has_tail="{self.has_tail}">'


dog = Dog("Ray")
print(dog)  # <Dog name=Ray type="Animal" paws="4" has_tail="True">
print()

print(xmltodict.unparse({"Dog": dog.__dict__}, pretty=True))
# <?xml version="1.0" encoding="utf-8"?>
# <Dog>
# 	<name>Ray</name>
# 	<type>Animal</type>
# 	<paws>4</paws>
# 	<has_tail>True</has_tail>
# </Dog>
