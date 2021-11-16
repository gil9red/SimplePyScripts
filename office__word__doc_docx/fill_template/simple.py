#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT

# pip install python-docx
import docx


from_filename = 'template.docx'
to_filename = 'simple.docx'


REPLACING = {
    '${title}': 'My pretty title!',
    '${datetime}': DT.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
}

doc = docx.Document(from_filename)
for p in doc.paragraphs:
    for k, v in REPLACING.items():
        if k in p.text:
            new_text = p.text.replace(k, v)
            p.text = new_text

doc.save(to_filename)
