# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# print('{one} * {one} {two}'.format(one="45", two="Bugaga"))


# import re
# import os
# # file_name = input("File name: ")
# file_name = "D:\hosts.txt"
# if os.path.exists(file_name):
#     with open(file_name) as file:
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



# import re
# text = """
# Предоставляет методы для управления дата и значения времени, связанных с файлом 11 11.
# """
#
# words = re.findall(r"\b\w+\b", text)
# print("Words: {}\nCount: {}".format(words, len(words)))
# word_count = Counter(words)
# for word, c in word_count.items():
#     print("Word: '{}', count: {}".format(word, c))


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
# # img.save("pil-basic-example.png")
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


# # Sort / Сортировка
# # https://wiki.python.org/moin/HowTo/Sorting
# import random
# l = [x for x in range(20)]
# random.shuffle(l)
# print("List: %s" % l)
# l.sort()
# print("Sorted list: %s" % l)
# l.sort(reverse=True)
# print("Reversed Sorted list: %s" % l)
#
# print()
# m = [x for x in range(20)]
# random.shuffle(m)
# print("Sorted list: %s" % sorted(m))
# print("Reversed Sorted list: %s" % sorted(m, reverse=True))
#
#
# class Student:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#
#     def __repr__(self):
#         return "%s (%d)" % (self.name, self.age)
#
#
# students = list()
# students.append(Student("Вася", 15))
# students.append(Student("Аня", 16))
# students.append(Student("Петя", 14))
# students.append(Student("Эдуарт", 25))
# students.append(Student("Таня", 16))
# students.append(Student("Саша", 15))
# print(students)
#
# students.sort(key=lambda x: x.age)  # Sorted by 'age'
# print(students)
#
# students.sort(key=lambda x: x.age, reverse=True)  # Sorted by 'age'
# print(students)
#
#
# students.sort(key=lambda x: x.name)  # Sorted by 'name'
# print(students)
#
#
# print()
# words = ["he", "He", "Ab", "ab", "Cc", "cC"]
# print("Words: {0}".format(words))
# print("Sorting:")
# print(sorted(words))
# print(sorted(words, reverse=True))
# print()
#
# # Sorting insensitive
# print("Sorting insensitive:")
# print(sorted(words, key=str.lower))  # or print(sorted(words, key=lambda x: x.lower()))
# print(sorted(words, key=str.lower, reverse=True))  # or print(sorted(words, key=lambda x: x.lower(), reverse=True))


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


# # __slots__:
# # This class variable can be assigned a string, iterable, or sequence of strings with variable names used by
# # instances. If defined in a new-style class, __slots__ reserves space for the declared variables and prevents the
# # automatic creation of __dict__ and __weakref__ for each instance. (Added in Python version 2.2)
# class Foo:
#     __slots__ = ["fus", "ro", "dah"]
#     dovakin = True
#
# f = Foo()
# f.fus = 1
# f.ro = 2
# # f.dah = 2
# print(f.dovakin)
# print(f.fus)
# print(f.ro)
# print(f.dah)  # AttributeError: dah -- dah is not determined
# # f.new_var = 1  # AttributeError: 'Foo' object has no attribute 'new_var'
#
# class Bar:
#     __slots__ = []
#     name = "Dova"
#
# b = Bar()
# print(b.name)
# # b.new_var = 1  # AttributeError: 'Foo' object has no attribute 'new_var'


## Example of using pipe module
# https://github.com/JulienPalard/Pipe
# ru: http://habrahabr.ru/post/117679/
import pipe

if __name__ == '__main__':
    print((i for i in range(10)) | pipe.as_list)  # tuple to list
    print([i for i in range(10)] | pipe.as_tuple)   # list to tuple
    print(((1,1), ('a', 2), (3, 'd')) | pipe.as_dict)  # tuple to dict

    print()
    # list of even numbers
    l = (i for i in range(10)) | pipe.where(lambda x: x % 2 is 0) | pipe.as_list
    c = l | pipe.count  # count elements
    print("List: {}, count: {}".format(l, c))
    print()

    # custom pipe:
    @pipe.Pipe
    def custom_add(x):
        return sum(x)

    print([1,2,3,4] | custom_add)  # = 10
