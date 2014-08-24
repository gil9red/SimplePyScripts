# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# print('{one} * {one} {two}'.format(one="45", two="Bugaga"))


# import base64
# print(base64.b64decode("VFJBQ0sx").decode("utf8"))
# print(base64.b64decode("MTEyMg==").decode("utf8"))
# print(base64.b64decode("MzIx").decode("utf8"))


# import datetime as dt
# import time
#
# while True:
#     cur_time = dt.datetime.now().time()
#     print("Current time is: %s" % cur_time.strftime("%H:%M:%S"), end='\r')
#     # print("Current time is: %s" % cur_time, end='\r')
#     time.sleep(0.5)  # every 0.5 second (500 millisecond)


# import zipfile
# import os
# file_name = input("Path to zip: ")
# if not os.path.exists(file_name):
#     print("File {} not exist!".format(file_name))
#
# with zipfile.ZipFile(file_name, mode='r') as zf:
#     for file_info in zf.filelist:
#         print(file_info.filename)


# import hashlib
# print("Algorithms guaranteed (all platforms):")
# print(hashlib.algorithms_guaranteed)
# print(sorted(set([x.lower()
#                   for x in hashlib.algorithms_guaranteed])),
#       end='\n\n')
#
# print("Algorithms available:")
# print(hashlib.algorithms_available)
# print(sorted(set([x.lower()
#                   for x in hashlib.algorithms_available])),
#       end='\n\n')
#
# md5 = hashlib.md5()
# # or: md5 = hashlib.new("md5")
# text = "Привет мир!".encode()
# md5.update(text)
# print(md5.hexdigest(), end='\n\n')
#
# sha1 = hashlib.new("sha1")
# # sha1 = hashlib.sha1()
# sha1.update(text)
# print(sha1.hexdigest(), end='\n\n')
#
# import binascii
# dk = hashlib.pbkdf2_hmac('sha256', b'password', b'salt', 100000)
# print(binascii.hexlify(dk))


# import random
# direction = ["up", 'down', 'left', 'right']
# for i in range(10):
#     print("Directions: %s, random direction = %s" % (direction, random.choice(direction)))
#
# print(random.random())  # rand float number
# print(random.randrange(5))  # rand int number
# print(random.randrange(0, 10))  # rand int number
# print(random.uniform(1, 10))  # rand float number
#
# print("Directions: %s" % direction)
# random.shuffle(direction)  # shuffle list
# print("Shuffle directions: %s" % direction)
#
# print(random.sample(direction, 2))  # select two element


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


# # Напишите программу, которая выводит на экран числа от 1 до 100. При этом вместо чисел, кратных трем, программа
# # должна выводить слово «Fizz», а вместо чисел, кратных пяти — слово «Buzz». Если число кратно и 3, и 5, то программа
# # должна выводить слово «FizzBuzz»
# for num in range(1, 100 + 1):
#     if num % 15 is 0:
#         print("FizzBuzz")
#     elif num % 3 is 0:
#         print("Fizz")
#     elif num % 5 is 0:
#         print("Buzz")
#     else:
#         print(num)


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
