__author__ = 'ipetrash'


# __author__ = 'ipetrash'
# 
# 
# """Скрипт отправляет win7 в режим гипернации (спящий режим)"""
# 
# 
# if __name__ == '__main__':
#     import os
#     os.system(r'%windir%\system32\rundll32.exe powrprof.dll,SetSuspendState Hibernate')


# def from_ghbdtn(text):
#     """ Convert
#       "b ,skb ghj,ktvs c ujcntdjq" -> "и были проблемы с гостевой"
#       "ghbdtn" -> "привет"
#     """
# 
#     en_keyboard = 'qwertyuiop[]asdfghjkl;\'\zxcvbnm,./`?'
#     ru_keyboard = 'йцукенгшщзхъфывапролджэ\ячсмитьбю.ё,'
# 
#     result = ''
# 
#     for c in text:
#         en_index = en_keyboard.find(c.lower())
#         if en_index != -1:
#             result += ru_keyboard[en_index]
#         else:
#             result += c
# 
#     return result
# 
# 
# text = ' b ,skb ghj,ktvs c ujcntdjq dhjlt ,s? gjcvjnhb '
# print(text)
# print(from_ghbdtn(text))



# TODO: пример работы с requests


## TODO: lived time
# import datetime
# my_bd = datetime.datetime(day=18, month=8, year=1992)
## my_bd = datetime.datetime(day=28, month=1, year=1993)
# my_life = datetime.datetime.today() - my_bd
#
# print('lived time: days = {} <=> seconds = {}'.format(my_life.days, my_life.days * 24 * 60 * 60))


# # TODO: пример работы с networkx
# # http://networkx.github.io/
# # http://networkx.github.io/documentation/latest/gallery.html
# # http://networkx.github.io/documentation/latest/reference/index.html
# # http://habrahabr.ru/post/125898/
# # http://habrahabr.ru/post/129344/
#
# import networkx as nx
# G = nx.Graph()
# G.add_edge('A', 'B', weight=4)
# G.add_edge('B', 'D', weight=2)
# G.add_edge('A', 'C', weight=3)
# G.add_edge('C', 'D', weight=4)
# print(nx.shortest_path(G, 'A', 'D', weight='weight'))


# http://habrahabr.ru/sandbox/84639/
# https://github.com/dimka665/vk
# https://pypi.python.org/pypi/vk/1.5
#
# import vk
#
# # vkapi = vk.API(app_id='app_id', user_login='+login', user_password='password')
# # or
# vkapi = vk.API(access_token='access_token')
# print(vkapi.getServerTime())
# profiles = vkapi.users.get(user_id=1)
# print(profiles[0]['last_name'])
# # vkapi.wall.post(message="Hello, world")


# TODO: нарисовать какой-нибудь фрактал
# https://ru.wikipedia.org/wiki/Фрактал
# https://ru.wikipedia.org/wiki/Множество_Мандельброта
# https://ru.wikipedia.org/wiki/Кривая_Коха
# http://algolist.manual.ru/graphics/fracart.php


# TODO: service pastebin.com
# http://pastebin.com/
# http://pastebin.com/api
# https://pypi.python.org/pypi/Pastebin/1.1.1


# TODO: service parse.com
# https://parse.com
# https://parse.com/docs/api_libraries
# https://github.com/dgrtwo/ParsePy
# http://habrahabr.ru/post/246989/


# import requests
#
# url = 'http://www.prog.org.ru/index.php'
# login = '*****'
# psw = '******'
#
# r = requests.get(url, auth=(login, psw))
# # print(r.status_code)
# # print(r.headers['content-type'])
# # print(r.encoding)
# print(r.text)
# # print(r.json())
#
# print('\n\n')
#
# from grab import Grab
# g = Grab()
# g.setup(post={'login': login, 'password': psw})
# g.go(url)
# print(g.response.body)


# # http://pythonworld.ru/moduli/modul-calendar.html
# # https://docs.python.org/3/library/calendar.html
# import calendar
# a = calendar.LocaleHTMLCalendar(locale='Russian_Russia')
#
# with open('calendar.html', 'w', encoding='utf-8') as g:
#     g.write(a.formatyear(2014, width=4))


# # TODO: сделать парсер для получения значения тегов
# # http://www.emvlab.org/tlvutils/?data=5F2A0206435F360102
# # https://ru.wikipedia.org/wiki/X.690
#
#
# def get_id_class_ber_desk(id_class_ber):
#     if id_class_ber == '00':
#         return "Universal"
#     elif id_class_ber == '01':
#         return "Application"
#     elif id_class_ber == '10':
#         return "Context-specific"
#     elif id_class_ber == '11':
#         return "Private"
#
#
# def get_id_type_ber_desk(id_type_ber):
#     if id_type_ber == '0':
#         return "Primitive"
#     elif id_type_ber == '1':
#         return "Constructed"
#     else:
#         raise Exception('id_type_ber может быть равным или 0, или 1.')
#
#
# # url: https://en.wikipedia.org/wiki/X.690, table "Universal Class Tags"
# UNIVERSAL_CLASS_TAGS = {
#     '0': 'EOC (End-of-Content)',
#     '1': 'BOOLEAN',
#     '2': 'INTEGER',
#     '3': 'BIT STRING',
#     '4': 'OCTET STRING',
#     '5': 'NULL',
#     '6': 'OBJECT IDENTIFIER',
#     '7': 'Object Descriptor',
#     '8': 'EXTERNAL',
#     '9': 'REAL (float)',
#     'A': 'ENUMERATED',
#     'B': 'EMBEDDED PDV',
#     'C': 'UTF8String',
#     'D': 'RELATIVE-OID',
#     'E': '(reserved)',
#     'F': '(reserved)',
#     '10': 'SEQUENCE and SEQUENCE OF',
#     '11': 'SET and SET OF',
#     '12': 'NumericString',
#     '13': 'PrintableString',
#     '14': 'T61String',
#     '15': 'VideotexString',
#     '16': 'IA5String',
#     '17': 'UTCTime',
#     '18': 'GeneralizedTime',
#     '19': 'GraphicString',
#     '1A': 'VisibleString',
#     '1B': 'GeneralString',
#     '1C': 'UniversalString',
#     '1D': 'CHARACTER STRING',
#     '1E': 'BMPString',
#     '1F': '(use long-form)',
# }
#
#
# def get_id_tag_ber_desk(id_tag_hex_ber):
#     # Удаляем пробелы с краев, удаляем префикс '0x, переводим в верхний регистр
#     tag_hex = id_tag_hex_ber.strip().lstrip('0x').upper()
#     return UNIVERSAL_CLASS_TAGS.get(tag_hex)
#
#
# def split_id_ber(id_hex_int):
#     def bit_value(num, pos):
#         return str((num & (1 << pos)) >> pos)
#
#     def bit_values(num, begin, end):
#         return ''.join([bit_value(num, i - 1) for i in range(begin, end - 1, -1)])
#
#     b5_b1 = bit_values(id_hex_int, 5, 1)
#     b6 = bit_value(id_hex_int, 6)
#     b8_b7 = bit_values(id_hex_int, 8, 7)
#
#     return (
#         b8_b7,  # Class
#         b6,  # Type
#         b5_b1  # Tag
#     )
#
#
# if __name__ == '__main__':
#     data_hex = '130B5465737420557365722031'
#     # print(data_hex)
#
#     id_hex_ber = data_hex[0:2]
#     # print("id: " + id_hex_ber)
#
#     id_bin_ber = bin(int(id_hex_ber, 16))[2:].zfill(8)
#     # print("id bin: " + id_bin_ber)
#
#     id_hex_int = int(id_hex_ber, 16)
#
#
#     id_class_ber, id_type_ber, id_tag_bin_ber = split_id_ber(id_hex_int)
#     # print("id_class: " + id_class_ber, end=" -> ")
#     id_class_desk_ber = get_id_class_ber_desk(id_class_ber)
#
#     # print("id_type: " + id_type_ber, end=" -> ")
#     id_type_desk_ber = get_id_type_ber_desk(id_type_ber)
#
#     # print("id_tag: " + id_tag_bin_ber, end=" -> ")
#     id_tag_dec_ber = int(id_tag_bin_ber, 2)
#     id_tag_hex_ber = hex(id_tag_dec_ber)
#     # print(str(id_tag_dec_ber) + " -> " + id_tag_hex_ber)
#
#     id_tag_desk_ber = get_id_tag_ber_desk(id_tag_hex_ber)
#
#
#     obj = {
#         'data_tlv': data_hex,
#         'id': {
#             'hex': id_hex_ber,
#             'bin': id_bin_ber,
#             'dec': id_hex_int,
#             'class': {
#                 'value': id_class_ber,
#                 'desk': id_class_desk_ber,
#             },
#             'type': {
#                 'value': id_type_ber,
#                 'desk': id_type_desk_ber,
#             },
#             'tag': {
#                 'bin': id_tag_bin_ber,
#                 'dec': id_tag_dec_ber,
#                 'hex': id_tag_hex_ber,
#                 'desc': id_tag_desk_ber,
#             },
#         },
#     }
#
#     import json
#     str_json_obj = json.dumps(obj, sort_keys=True, indent=4)
#     print(str_json_obj)


# TODO: ascii -> hex and hex -> ascii
# def ascii2hex(s, prefix_hex='0x'):
#     """
#     ASCII -> HEX
#     RU -> 0x5255
#     """
#
#     ascii_str = s.encode('ascii')
#
#     hex_str = ''
#
#     for c in ascii_str:
#         hex_str += str(hex(c)).lstrip('0x')
#
#     return prefix_hex + hex_str
#
#
# def hex_str2ascii(hex_str):
#     """
#     HEX -> ASCII
#     0x5255 -> RU
#     """
#
#     hex_str = hex_str.lstrip('0x')
#
#     ascii_str = ''
#     for i in range(len(hex_str)):
#         if i % 2:
#             hex_num = int(hex_str[i - 1] + hex_str[i], base=16)
#             ascii_str += chr(hex_num)
#
#     return ascii_str
#
#
# my_str = 'RUASCIIEN'
#
# hex_str = ascii2hex(my_str)
# ascii_str = hex_str2ascii(hex_str)
#
# print('{} -> {}'.format(my_str, hex_str))
# print('{} -> {}'.format(hex_str, ascii_str))
#
#
# import binascii
# my_str = 'RUASCIIEN'
# print(binascii.b2a_hex(my_str.encode('ascii')))


# # TODO: добавить в примеры работы с регулярными выражениями
#
# def convert_url_githubio_to_repo(url):
#     # Функция конвертирует путь из проекта github.io в репозиторий проекта github.com
#     # http://gabrielecirulli.github.io/2048/ -> https://github.com/gabrielecirulli/2048/
#
#     import re
#     pattern = r'http://(.+).github.io/(.+)/'
#     search = re.search(pattern, url)
#
#     user = search.group(1)
#     repo = search.group(2)
#     return 'https://github.com/{}/{}/'.format(user, repo)
#
#
# url = 'http://gabrielecirulli.github.io/2048/'
# url_repo = convert_url_githubio_to_repo(url)
# print(url)
# print(url_repo)


# TODO: больше примеров работы с модулями py
# http://pythonworld.ru/karta-sajta


# TODO: воспроизведение музыкальных файлов
# # Window only
# # https://docs.python.org/3/library/winsound.html
# import winsound
# # Play Windows exit sound.
# winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
#
# # Probably play Windows default sound, if any is registered (because
# # "*" probably isn't the registered name of any sound).
# winsound.PlaySound("*", winsound.SND_ALIAS)
#
# winsound.PlaySound('Gorillaz-Clint_Eastwood.wav', winsound.SND_FILENAME)


# TODO: pretty-print
# https://docs.python.org/3.4/library/pprint.html
# import pprint
#
# # stuff = ['spam', 'eggs', 'lumberjack', 'knights', 'ni']
# # stuff.insert(0, stuff[:])
# # pp = pprint.PrettyPrinter(indent=4)
# # pp.pprint(stuff)
# #
# # pp = pprint.PrettyPrinter(width=41, compact=True)
# # pp.pprint(stuff)
#
# # tup = ('spam', ('eggs', ('lumberjack', ('knights', ('ni', ('dead', ('parrot', ('fresh fruit',))))))))
# # pp = pprint.PrettyPrinter(depth=3)
# # pp.pprint(tup)


# __author__ = 'ipetrash'
#
# # Суть задачи в том, чтобы из англо-латинского словаря сделать латино-английский.
# #
# # Примеры тестов:
# #  Входные данные
# #  3
# #  apple - malum, pomum, popula
# #  fruit - baca, bacca, popum
# #  punishment - malum, multa
# #
# #  Выходные данные
# #  7
# #  baca - fruit
# #  bacca - fruit
# #  malum - apple, punishment
# #  multa - punishment
# #  pomum - apple
# #  popula - apple
# #  popum - fruit
#
#
# if __name__ == '__main__':
# la_en = {}
#
#     # Открываем для чтения
#     with open('input.txt', mode='r') as f:
#         # Первая строка -- количество записей
#         count = int(f.readline())
#
#         # Получаем count строк
#         for i in range(count):
#             # Получим строку вида: baca - fruit
#             row = f.readline().strip()
#
#             # Разделим строку на две части
#             en, la_words = row.split(' - ')
#
#             # Из правой части (латинские слова) разделяем на список
#             # и добавляем в словарь, в котором ключом является латинское
#             # слово, а значением -- список английский слов
#             for la in la_words.split(', '):
#                 # Если слово la уже есть в словаре, то добавляем английское слово
#                 # в список в правой части, иначе создаем список
#                 if la in la_en:
#                     la_en[la].append(en)
#                 else:
#                     la_en[la] = [en]
#
#     # Открываем для записи
#     with open('output.txt', mode='w') as f:
#         # Первая строка -- количество записей
#         count = len(la_en)
#         f.write(str(count) + '\n')
#
#         # Перебираем список отсортированных латинский слов
#         for la in sorted(la_en.keys()):
#             f.write('{} - {}\n'.format(la, ', '.join(la_en[la])))


# import re
# import os
# # file_name = input("File name: ")
# file_name = "D:\hosts.txt"
# if os.path.exists(file_name):
# with open(file_name) as file:
# for row in file:
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


# # TODO: добавление примеров:
# http://jenyay.net/Matplotlib/Date
# http://jenyay.net/Matplotlib/Text
# http://jenyay.net/Matplotlib/Xkcd
# http://jenyay.net/Matplotlib/Locators
# http://jenyay.net/Matplotlib/LogAxes


# TODO: Сумма чисел
# l = [1, 2, 3, 4]
# print(sum(l))


# TODO: Среднее значение суммы чисел
# l = [1, 2, 3, 4]
# print(sum(l))
# print(sum(l) / len(l))


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
