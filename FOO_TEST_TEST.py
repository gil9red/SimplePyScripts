from collections import Counter

__author__ = 'ipetrash'


# def getprint(str="hello world!"):
#     print(str)
#
# def decor(func):
#     def wrapper(*args, **kwargs):
#         print("1 begin: " + func.__name__)
#         print("Args={} kwargs={}".format(args, kwargs))
#         f = func(*args, **kwargs)
#         print("2 end: " + func.__name__ + "\n")
#         return f
#     return wrapper
#
# def predecor(w="W"):
#     print(w, end=': ')
#     return decor
#
# # getprint = decor(getprint)
# # getprint()
#
# getprint("Py!")
#
#
# def rgb2hex(get_rgb_func):
#     def wrapper(*args, **kwargs):
#         r, g, b = get_rgb_func(*args, **kwargs)
#         return '#{:02x}{:02x}{:02x}'.format(r, g, b)
#     return wrapper
#
# class RGB:
#     def __init__(self):
#         self._r = 0xff
#         self._g = 0xff
#         self._b = 0xff
#
#     def getr(self):
#         return self._r
#     def setr(self, r):
#         self._r = r
#     r = property(getr, setr)
#
#     def getg(self):
#         return self._g
#     def setg(self, g):
#         self._g = g
#     g = property(getg, setg)
#
#     def getb(self):
#         return self._b
#     def setb(self, b):
#         self._b = b
#     b = property(getb, setb)
#
#     @predecor("Hello")
#     def setrgb(self, r, g, b):
#         self.r, self.g, self.b = r, g, b
#
#     @decor
#     @rgb2hex
#     def getrgb(self):
#         return (self.r, self.g, self.b)
#
# rgb = RGB()
# print(rgb.r)
# rgb.setrgb(0xff, 0x1, 0xff)
# print(rgb.getrgb())

# @decor
# def foo(a, b):
#     print("{} ^ {} = {}".format(a, b, (a ** b)))
#
# foo(2, 3)
#
# foo(b=3, a=2)

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


# TODO: наложение "водяного знака" на изображение
