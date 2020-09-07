#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/madmaze/pytesseract


import re

# pip install pillow
from PIL import Image

# pip install pytesseract
# Tesseract.exe from https://github.com/UB-Mannheim/tesseract/wiki
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# Simple image to string
img = Image.open('test.jpg')
text = pytesseract.image_to_string(img, lang='eng')

text = re.sub(r'(\s){2,}', '\1', text)
print(text)
# At this Time. two Great Empires struggled
# for Dominion over Ivalice:Archadia in the East. Rozarria. the West.
# AIChdadladT he Invasion of the Kingdom of NabradiawasArchadia's first Step RRs s. westward M Cigale
# abradiaWith Cord Rasler's area omeland con rit aNthe Hell-Fires of War. it aa TaeWa eeiad Velma Veerwould soon mete out a like Fate to Valmasca.
# KOZarrlaThe Fall of the Fortress at Nalbina
# tolled the Destruction of the greater
# part of Dalmasca’'s f orces.
