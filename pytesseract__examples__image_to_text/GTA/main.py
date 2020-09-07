#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install pillow
from PIL import Image

# pip install pytesseract
# tesseract.exe from https://github.com/UB-Mannheim/tesseract/wiki
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


file_name = 'RuFjPBg.png'
img = Image.open(file_name)

text = pytesseract.image_to_string(img, lang='eng')
print(repr(text))
# '.\nCheat activated'

print(text)
# .
# Cheat activated
