# -*- coding: utf-8 -*-


__author__ = 'ipetrash'


# TODO: получение курса валют 1 USD -> ? RUB: http://news.yandex.ru/quotes/1.html


# import re
# import os
# # file_name = input("File name: ")
# file_name = "D:\hosts.txt"
# if os.path.exists(file_name):
# with open(file_name) as file:
#         for row in file:
#             m = re.search(r"(\d{1,3}).(\d{1,3}).(\d{1,3}).(\d{1,3})(/(\d{1,3}))?", row)
#             if m:
#                 ip = m.group(0)
#                 ip_1 = m.group(1)
#                 ip_2 = m.group(2)
#                 ip_3 = m.group(3)
#                 ip_4 = m.group(4)
#                 ip_5 = m.group(6)  # m.group(5) -- this (/([0-9]{1,3})), m.group(6) -- ([0-9]{1,3})
#                 if ip_5:
#                     print("ip: '{}':\n    1:'{}' 2:'{}' 3:'{}' 4:'{}' 5:'{}'".format(ip, ip_1, ip_2, ip_3, ip_4, ip_5))
#                 else:
#                     print("ip: '{}':\n    1:'{}' 2:'{}' 3:'{}' 4:'{}'".format(ip, ip_1, ip_2, ip_3, ip_4))
#                 print()


# # Overlay "watermark" image / Наложение "водяного знака" на изображение
# import os
# from PIL import Image, ImageDraw, ImageFont
#
# # from PIL import Image, ImageDraw
# # text = "Hello, PIL!!!"
# # color = (0, 0, 120)
# # img = Image.new('RGB', (100, 50), color)
# # imgDrawer = ImageDraw.Draw(img)
# # imgDrawer.text((10, 20), text)
# # img.save("pil_example-basic-example.png")
#
# path = r"C:\Users\ipetrash\Desktop\pic.png"
# # path = input("Input path: ")
# path = os.path.normpath(path)
# if os.path.exists(path):
#     print("File: %s" % path)
#
#     image = Image.open(path)
#     width, height = image.size
#     # image.show()
#
#     drawer = ImageDraw.Draw(image)
#     font = ImageFont.truetype("arial.ttf", 25)
#     text = "Hello World!"
#     width_text, height_text = font.getsize(text)
#     for i in range(0, width, width_text * 2):
#         for j in range(0, height, height_text * 2):
#             drawer.text((i, j), text, font=font, fill=(0x00, 0xff, 0x00))
#
#     image.show()
#     input("")
#     # image.save(path)


# import sqlite3
# # https://docs.python.org/3.4/library/sqlite3.html
# path = r"C:\Users\ipetrash\Desktop\teller\kmaksimov_NDC.sdb"
# conn = sqlite3.connect(path)
# # result = tuple(row for row in conn .cursor().execute("SELECT * FROM BNA_Demoninations"))
# # for s in result:
# #     print(s)
#
# # cursor = conn .cursor()
# # for row in cursor.execute("SELECT * FROM BNA_Demoninations"):
# #     print(row)
#
# c = conn.cursor()
# result = tuple(row for row in c.execute("SELECT * FROM BNA_Demoninations"))
# print(result)
# print(sorted(result, key=lambda x: x[1]))  # sorting by the second value
#
# # Way to get a list of column names
# print()
# # 1
# print("Column names: {0}".format(c.description))
#
# # 2
# result = tuple(row for row in c.execute("PRAGMA table_info('BNA_Demoninations')"))
# print("Column names: {0}".format(result))
#
# # 3
# conn.row_factory = sqlite3.Row
# c = conn.execute('select * from BNA_Demoninations')
# row = c.fetchone()  # instead of cursor.description
# names = row.keys()
# print("Column names: {0}".format(names))


# # TODO: добавление примеров:
# http://jenyay.net/Matplotlib/Date
# http://jenyay.net/Matplotlib/Text
# http://jenyay.net/Matplotlib/Xkcd
# http://jenyay.net/Matplotlib/Locators
# http://jenyay.net/Matplotlib/LogAxes


# ## Quality Control
# # doctest
# def average(values):
#     """Computes the arithmetic mean of a list of numbers.
#
#     >>> print(average([20, 30, 70]))
#     40.0
#     """
#     return sum(values) / len(values)
#
# import doctest
# doctest.testmod()   # automatically validate the embedded tests
#
# # unittest
# import unittest
#
# class TestStatisticalFunctions(unittest.TestCase):
#
#     def test_average(self):
#         self.assertEqual(average([20, 30, 70]), 40.0)
#         self.assertEqual(round(average([1, 5, 7]), 1), 4.3)
#         with self.assertRaises(ZeroDivisionError):
#             average([])
#         with self.assertRaises(TypeError):
#             average(20, 30, 70)
#
# unittest.main() # Calling from the command line invokes all tests


# TODO: https://docs.python.org/3/tutorial/stdlib2.html
# import textwrap
# text = 'Придумать простое приложение и реализовать его с помощью TDD (используя unit-тесты)'
# print(textwrap.fill(text, width=45))


# TODO: придумать простое приложение и реализовтаь его с помощью TDD (используя unit-тесты)


# TODO: Flask
# "Мега-Учебник Flask, Часть 1: Привет, Мир!": http://habrahabr.ru/post/193242/
# http://ru.wikibooks.org/wiki/Flask


# TODO: Excel
# "Интеграция MS Excel и Python": http://habrahabr.ru/post/232291/


# TODO: tornado
# "Современный Торнадо: распределённый хостинг картинок в 30 строк кода":
# http://habrahabr.ru/post/230607/


# TODO: визуализация связей в вк и linkedin:
# http://habrahabr.ru/post/221251/
# https://github.com/stleon/vk_friends


# TODO: Webmoney API
# http://habrahabr.ru/post/222411/


# TODO: Основы создания 2D персонажа в Godot
# https://github.com/okamstudio/godot/
# "Игровой движок Godot отдали в общественное пользование": http://habrahabr.ru/post/212109/
#
# "Часть 1: компилирование игрового движка, создание проекта и анимация покоя героя":
# http://habrahabr.ru/post/212583/
#
# "Часть 2: компилирование шаблонов, немного о GDScript, движение и анимация героя":
# http://habrahabr.ru/post/212837/


# TODO: "Экспорт Избранного на Хабре в PDF": http://habrahabr.ru/post/208802/
# Оригинал: https://github.com/vrtx64/fav2pdf
# Форк: https://github.com/icoz/fav2pdf


# TODO: Работа с буфером обмена: pyperclip
# http://stackoverflow.com/questions/11063458/python-script-to-copy-text-to-clipboard


# TODO: brutforce Instagram
# http://habrahabr.ru/post/215829/
