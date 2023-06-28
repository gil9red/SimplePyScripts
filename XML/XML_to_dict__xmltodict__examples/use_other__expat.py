#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/martinblech/xmltodict


# pip install xmltodict
import xmltodict

# You can pass an alternate version of `expat` (such as `defusedexpat`) by using the `expat` parameter. E.g:
import defusedexpat


doc = xmltodict.parse("<a>hello</a>", expat=defusedexpat.pyexpat)
print(doc)  # OrderedDict([('a', 'hello')])
