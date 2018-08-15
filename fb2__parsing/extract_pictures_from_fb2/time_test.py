#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from fb2_pictures__using_lxml import do as do_lxml
from fb2_pictures__using_re import do as do_using_re
from fb2_pictures__using_xml_expat import do as do_xml_expat
from fb2_pictures__using_xml_etree import do as do_xml_etree


file_name = '../input/Непутевый ученик в школе магии 1. Зачисление в школу (Часть 1).fb2'
count = 10

from timeit import timeit
print('LXML:      {:.3f} secs'.format(timeit('do_lxml(file_name, False)', globals=globals(), number=count)))
print('XML EXPAT: {:.3f} secs'.format(timeit('do_xml_expat(file_name, False)', globals=globals(), number=count)))
print('XML.ETREE: {:.3f} secs'.format(timeit('do_xml_etree(file_name, False)', globals=globals(), number=count)))
print('RE:        {:.3f} secs'.format(timeit('do_using_re(file_name, False)', globals=globals(), number=count)))
