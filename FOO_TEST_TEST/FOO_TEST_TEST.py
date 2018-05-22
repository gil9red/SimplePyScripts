#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# # transliterate
# # транслитерация
#
# # pip install transliterate
# from transliterate import translit
# text = "Тбилиси"
# translit(text, 'en')
# print(text)
#
#
# # import transliterate
# # name_input = 'Hello World Привет мир'
# # try:
# #     name = transliterate.translit(name_input, reversed=True)
# # except transliterate.exceptions.LanguageDetectionError:
# #     name = name_input
# #
# # print(name)
#
#
# # print(translit(u"Тбилиси", 'ru', reversed=True))
# # Tbilisi
# #


# TODO: openpyxl: http://openpyxl.readthedocs.io/en/stable/usage.html#inserting-an-image
# wb = openpyxl.Workbook()
# ws = wb.get_active_sheet()
#
# from openpyxl.drawing.image import Image
#
# ws['A1'] = 'You should see three logos below'
#
# # create an image
# img = Image('input.jpg')
#
# # add to worksheet and anchor next to cells
# ws.add_image(img, 'A1')
# wb.save('logo.xlsx')
