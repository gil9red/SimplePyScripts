#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from fb2_pictures__using_lxml import do as do_lxml
from fb2_pictures__using_xml_expat import do as do_xml_expat
from fb2_pictures__using_xml_etree import do as do_xml_etree
from fb2_pictures__using_xml_sax import do as do_xml_sax
from fb2_pictures__using_re import do as do_using_re


file_name = '../input/Непутевый ученик в школе магии 1. Зачисление в школу (Часть 1).fb2'
count = 10

from timeit import timeit

runs = [
    ('LXML',      'do_lxml(file_name, debug=False)'),
    ('XML EXPAT', 'do_lxml(file_name, debug=False)'),
    ('XML.ETREE', 'do_lxml(file_name, debug=False)'),
    ('XML SAX',   'do_xml_sax(file_name, debug=False)'),
    ('REGEXP',    'do_using_re(file_name, debug=False)'),
]
runs_format = '{:%s} | {:.3f} secs' % (max(len(x[0]) for x in runs),)

for name, stmt in runs:
    print(runs_format.format(name, timeit(stmt, globals=globals(), number=count)))
