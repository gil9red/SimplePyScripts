#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install pypdf2
from PyPDF2 import PdfFileMerger


pdfs = ['1.pdf', '2.pdf', '3.pdf']

merger = PdfFileMerger()
for pdf in pdfs:
    merger.append(pdf)

merger.write("result.pdf")
merger.close()
