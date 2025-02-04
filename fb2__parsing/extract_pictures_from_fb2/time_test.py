#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from timeit import timeit

from fb2_pictures__using_lxml import do as do_lxml
from fb2_pictures__using_bs4 import do as do_bs4
from fb2_pictures__using_xml_expat import do as do_xml_expat
from fb2_pictures__using_xml_etree import do as do_xml_etree
from fb2_pictures__using_xml_etree_xpath import do as do_xml_etree_xpath
from fb2_pictures__using_xml_sax import do as do_xml_sax
from fb2_pictures__using_re import do as do_using_re
from fb2_pictures__using_str_find import do as do_using_str_find


file_name = "../input/Непутевый ученик в школе магии 1. Зачисление в школу (Часть 1).fb2"
count = 10

runs = [
    ("LXML", "do_lxml"),
    ("XML EXPAT", "do_xml_expat"),
    ("XML.ETREE", "do_xml_etree"),
    ("XML.ETREE xpath", "do_xml_etree_xpath"),
    ("XML SAX", "do_xml_sax"),
    ("REGEXP", "do_using_re"),
    ("STR FIND", "do_using_str_find"),
    ("BS4", "do_bs4"),
]
runs_format = "{:%s} | {:.3f} secs" % (max(len(x[0]) for x in runs),)

for name, stmt in runs:
    timing = timeit(stmt + "(file_name, debug=False)", globals=globals(), number=count)
    print(runs_format.format(name, timing))
"""
LXML      | 0.733 secs
XML EXPAT | 0.867 secs
XML.ETREE | 0.755 secs
XML SAX   | 1.014 secs
REGEXP    | 2.466 secs
STR FIND  | 1.210 secs
BS4       | 2.166 secs
"""
