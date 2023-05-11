#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from fb2_pictures__using_lxml import do as do_lxml
from fb2_pictures__using_bs4 import do as do_bs4
from fb2_pictures__using_xml_expat import do as do_xml_expat
from fb2_pictures__using_xml_etree import do as do_xml_etree
from fb2_pictures__using_xml_sax import do as do_xml_sax
from fb2_pictures__using_re import do as do_using_re


file_name = "../input/Непутевый ученик в школе магии 1. Зачисление в школу (Часть 1).fb2"
count = 10

from timeit import timeit

runs = [
    ("LXML", "do_lxml"),
    ("XML EXPAT", "do_xml_expat"),
    ("XML.ETREE", "do_xml_etree"),
    ("XML SAX", "do_xml_sax"),
    ("REGEXP", "do_using_re"),
    ("BS4", "do_bs4"),
]
runs_format = "{:%s} | {:.3f} secs" % (max(len(x[0]) for x in runs),)

for name, stmt in runs:
    timing = timeit(stmt + "(file_name, debug=False)", globals=globals(), number=count)
    print(runs_format.format(name, timing))
