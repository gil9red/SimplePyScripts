#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/madmaze/pytesseract


import re

# pip install googletrans
from googletrans import Translator

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

print('', '-' * 100, '', sep='\n')

from_lang = 'en'
to_lang = 'ru'

translator = Translator()
translation = translator.translate(
    text,
    src=from_lang,
    dest=to_lang
).text
print(translation)
# В это время. два Великие Империи боролись
# для Dominion над Ивалисом: Archadia на Востоке. Rozarria. Запад.
# AIChdadlad T он Invasion Королевства Nabradiawas Archadia это первый шаг RRs s. запад M Cigale
# Площадь abradia шнуром Rasler в omeland кон рит АН Ад-Пожары войны. это аа TaeWa eeiad Велма Veer вскоре вершить как судьба Valmasca.
# KOZarrla Падение крепости в Nalbina
# пробил уничтожение Большого
# часть F orces Dalmasca '»s.
