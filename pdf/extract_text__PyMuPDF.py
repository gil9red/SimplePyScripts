#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install PyMuPDF
import fitz


with fitz.open("merger__PyPDF2/1.pdf") as doc:
    items = []
    for page in doc:
        items.append(page.get_text())
    text = '\n'.join(items)

print(text)

