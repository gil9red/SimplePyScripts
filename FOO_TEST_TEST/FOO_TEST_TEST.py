#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'ipetrash'


# # Convertor githun pages url to github repo url
# # http://nemilya.github.io/coffeescript-game-life/html/game.html
# # https://github.com/nemilya/coffeescript-game-life
#
# import re
#
# github_pages_url = 'http://nemilya.github.io/coffeescript-game-life/html/game.html'
#
# match = re.search('https?://(.+)\.github.io/(.+)', github_pages_url)
# if match is not None:
#     user = match.group(1)
#     repo = match.group(2).split('/')[0]
#
#     github_repo_url = 'https://github.com/{}/{}'.format(user, repo)
#     print(github_repo_url)


# """У нас есть список сил и возможно комбинировать одновременно только две разные силы,
# причем повторов быть не должно -- ('Огонь', 'Молния') и ('Молния', 'Огонь') -- повторы."""
#
# import itertools
#
# # Комбинации сил, максимум за раз могут две учавствовать, плюс возможны только разные
# powers = ['Огонь', 'Молния', 'Лед', 'Воздух']
#
# # Все комбинации без повторов
# # Если нужны комбинации с повторами, используется itertools.product(powers, repeat=2)
# all_combo = itertools.combinations(powers, 2)
# for i, combo in enumerate(all_combo, 1):
#     print('{}. {} и {}'.format(i, *combo))


# # concurrency.py
# from collections import deque
# from time import time, sleep as sys_sleep
#
#
# # Взято: http://habrahabr.ru/post/243207/
#
#
# class coroutine(object):
#     """Делает из функции сопрограмму на базе расширенного генератора."""
#     _current = None
#
#     def __init__(self, callable):
#         self._callable = callable
#
#     def __call__(self, *args, **kwargs):
#         corogen = self._callable(*args, **kwargs)
#         cls = self.__class__
#         if cls._current is None:
#             try:
#                 cls._current = corogen
#                 next(corogen)
#             finally:
#                 cls._current = None
#         return corogen
#
#
# def sleep(timeout):
#     """Приостанавливает выполнение до получения события "таймаут истек"."""
#     corogen = coroutine._current
#     dispatcher.setup_timeout(corogen, timeout)
#     revent = yield
#     return revent
#
#
# class Dispatcher(object):
#     """Объект реализующий диспечер событий."""
#     def __init__(self):
#         self._pending = deque()
#         self._deadline = time() + 3600.0
#
#     def setup_timeout(self, corogen, timeout):
#         deadline = time() + timeout
#         self._deadline = min([self._deadline, deadline])
#         self._pending.append([corogen, deadline])
#         self._pending = deque(sorted(self._pending, key=lambda a: a[1]))
#
#     def run(self):
#         """Запускает цикл обработки событий."""
#         while len(self._pending) > 0:
#             timeout = self._deadline - time()
#             self._deadline = time() + 3600.0
#             if timeout > 0:
#                 sys_sleep(timeout)
#             while len(self._pending) > 0:
#                 if self._pending[0][1] <= time():
#                     corogen, _ = self._pending.popleft()
#                     try:
#                         coroutine._current = corogen
#                         corogen.send("timeout")
#                     except StopIteration:
#                         pass
#                     finally:
#                         coroutine._current = None
#                 else:
#                     break
#
# dispatcher = Dispatcher()
# run = lambda: dispatcher.run()
#
#
# @coroutine
# def hello(name, timeout):
#     while True:
#         yield from sleep(timeout)
#         print("Привет, {}!".format(name))
#
# hello("Петров", 2.0)
# hello("Иванов", 3.0)
# hello("Мир", 5.0)
# run()


# # Разбор примера шифрования с помощью справочника: https://ru.wikipedia.org/wiki/Криптосистема_с_открытым_ключом
# REFERENCE_GUIDE_NAME_NUM = {
#     'Королёв': '5643452',
#     'Орехов': '3572651',
#     'Рузаева': '4673956',
#     'Осипов': '3517289',
#     'Батурин': '7755628',
#     'Кирсанова': '1235267',
#     'Арсеньева': '8492746',
# }
#
# # Обратный словарь -- ключом будет число, а значением имя
# REFERENCE_GUIDE_NUM_NAME = {v: k for k, v in REFERENCE_GUIDE_NAME_NUM.items()}
#
# MESS = 'коробка'
#
#
# def encrypt(mess):
#     keys = REFERENCE_GUIDE_NAME_NUM.keys()
#     crypto_text_list = list()
#
#     for c in mess.lower():
#         encrypt_key = sorted(filter(lambda x: x[0].lower() == c, keys))[0]
#         crypto_text_list.append(REFERENCE_GUIDE_NAME_NUM[encrypt_key])
#
#     return '@'.join(crypto_text_list)
#
#
# def decrypt(encrypt_mess):
#     crypto_num_list = encrypt_mess.split('@')
#     mess = ''
#
#     for num in crypto_num_list:
#         mess += REFERENCE_GUIDE_NUM_NAME[num][0].lower()
#
#     return mess
#
# encrypt_mess = encrypt(MESS)
#
# print('Encrypt: {} -> {}.'.format(MESS, encrypt_mess))
# print('Decrypt: {} -> {}'.format(encrypt_mess, decrypt(encrypt_mess)))


# # Поиск мультсериалов 16+
# # Пример сериала: 'http://onlinemultfilmy.ru/bratya-ventura/'
#
# import time
# from grab import Grab
#
# g = Grab()
#
# # Перебор страниц с мультами
# for i in range(1, 82 + 1):
#     url_page = 'http://onlinemultfilmy.ru/multserialy/page/' + str(i)
#     print(url_page)
#
#     # Загрузка страницы с мультами
#     g.go(url_page)
#
#     # Перебор и загрузка мультов на странице
#     for url in g.doc.select('//div[@class="cat-post"]/a'):
#         g.go(url.attr('href'))
#
#         if g.doc.select('//*[@class="age_icon age_icon_16"]').count():
#             print('    ', url.attr('title'), url.attr('href'))
#
#         # Чтобы сервер не посчитал это дос атакой
#         time.sleep(2)


# # Удаление // комментариев и пробелов с табуляцией
# def rem(text):
#     line_list = list()
#
#     for line in text.strip().split('\n'):
#         line = line.strip()
#
#         if line.startswith('//'):
#             line = line[2:]
#
#         line = line.strip()
#         line_list.append(line)
#
#     return '\n'.join(line_list)
#
#
# r = rem("""
#
#     // Summary:
#     //     The account selection transaction unit is used for building transactions
#     //     in which the customer must select or identify an account on which the transaction
#     //     is to be performed. Several different methods are supported for identifying
#     //     the account. The method to be used is configured through the AccountSelectionMethod
#     //     property: see help for that property for more details.  The SelectAccount
#     //     method is the main top-level method called by Customer Transaction Objects
#     //     for performing account selection.
#
# """)
# print(r)
#
#
# import re
# r = r.replace('\n', ' ')
# r = re.sub('[ ]{2,}', '', r)
# import copy2clipboard
# copy2clipboard.to(r)
# print(r)
#
# import goslate
# gs = goslate.Goslate()
# print('\n', gs.translate(r, 'ru'))
#
# # from translate import Translator
# # translator = Translator(to_lang="ru")
# # translation = translator.translate(r)
# # print(translation)


# TODO: функцию перевода используя гугл-переводчик или даже скрипт, который будет запускаться в качестве
# процесса, вывод, которого будем читать и парсить. Вывод и будет содержать перевод или ошибку в специальном
# формате
# import urllib.parse
# urllib.parse.quote('grgr\nge\r')


# http://habrahabr.ru/post/192102/
# http://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html
#
# def gen_sudoku(n=3):
#     return [[((i*n + i//n + j) % (n*n) + 1) for j in range(n*n)] for i in range(n*n)]
#
# for row in gen_sudoku():
#     print(row)
#


# s = """
# - Robocop Versus The Terminator
#   Mortal Kombat 3
# - Dune - The Battle for Arrakis
# - Comix Zone
# @ Disney's Aladdin
# - Earthworm Jim 1, 2
# - Jungle Book, The
# - Sonic The Hedgehog 1, 2, 3
# - Lion King, The
# @ Theme Park
# - Tiny Toon Adventures - Acme All-Stars
# @ Mickey Mania - Timeless Adventures of Mickey Mouse
# @ Battletoads
# - Prince of Persia
#   Side Pocket
# - Boogerman
#   Flintstones, The
# - Zero the Kamikaze Squirrel
# @ Gargoyles
#   Weaponlord
# @ Vectorman
# - Michael Jackson's Moonwalker
#
#   Ultimate Mortal Kombat 3
# - Comix Zone
# - Earthworm Jim 2
# - Battletoads and Double Dragon
# @ Disney's Aladdin
# - Sonic The Hedgehog 2, 3
# - Earthworm Jim
# - Dune - The Battle for Arrakis
# - Boogerman
#   Lion King, The
# - Golden Axe III
# - Jungle Book, The
# - Robocop Versus The Terminator
# - Desert Strike - Return to the Gulf
# - Prince of Persia
#   Flintstones, The
# - Vectorman
# - Gargoyles
# """
#
# l = set()
#
# for c in s.split('\n'):
#     if c:
#         l.add(c[2:])
# print('\n'.join(l))
# quit()



# # Список игр: https://gist.github.com/gil9red/2f80a34fb601cd685353
#
# from grab import Grab
# from urllib.parse import quote_plus
#
#
# class DontFindGame(Exception):
#     pass
#
#
# def find_game(game_name):
#     """Скрипт ищет игру в стиме, и если находит, возвращает
#     кортеж вида: {title}, {price}, {href}
#     Если не находит, выкидывает исключение DontFindGame
#
#     """
#
#     print(game_name)
#
#     # Сортировка: релевантная, категории: игры, платформа: Windows, поиск: <game>
#     steam_url = 'http://store.steampowered.com/search/?sort_by=_ASC&category1=998&os=win&term='
#     url = steam_url + quote_plus(game_name)
#     print(url)
#
#     g = Grab()
#     g.go(url)
#
#     # print(g.response.code)
#
#     select = g.doc.select('//a[contains(@class, "search_result_row")]')
#
#     # for a in select:
#     #     title = a.select('div[contains(@class, "search_name")]/span[@class="title"]').text()
#     #     price = a.select('div[contains(@class, "search_price")]').text()
#     #     print(a.attr('href'), title, price)
#
#     if select.count():
#         # По идеи, первая игра в списке -- наша
#         # TODO: доработать: сравнивать title нашей игры с найденными, пока не найдем
#         # TODO: перед сравнением удалить все символы кроме a-zA-Z0-9 и привести к одному регистру
#         # TODO: некоторые игры могут найтись даже при не совпадении, например
#         # "Ведьмак" найдет как "The Witcher", и это правильно
#         a = select[0]
#         title = a.select('div[contains(@class, "search_name")]/span[@class="title"]').text()
#         price = a.select('div[contains(@class, "search_price")]').text()
#         price = tuple(price.split())
#         return title, price, a.attr('href')
#     else:
#         raise DontFindGame('Не получилось найти игру "{}".'.format(game_name))
#
#
# game = 'Max Payne 3'
# game = 'Dragon Age: Origins'
# game = 'Final Fantasy XIII'
# # game = 'What The Fuck?!'
#
# try:
#     game_info = find_game(game)
#     print(game_info)
#
# except DontFindGame as e:
#     print(e)
#
# except Exception as e:
#     print('Error:', e)




# def get_short_url(url):
#     """Функция возвращает короткую ссылку на url.
#     Для этого она использует сервис clck.ru
#
#     """
#
#     from urllib.request import urlopen
#
#     with urlopen('https://clck.ru/--?url=' + url) as rs:
#         return rs.read().decode()
#
#
# url = 'https://www.google.ru/search?q=short+url+python'
# print(get_short_url(url))


# class Student:
#     def __init__(self, name, group, age):
#         self.name = name
#         self.group = group
#         self.age = age
#
#
# list_students = []
# list_students.append(Student('Вася', 'АВ-1', 16))
# list_students.append(Student('Саша', 'АВ-1', 20))
# list_students.append(Student('Петя', 'АВ-1', 16))
# list_students.append(Student('Аня', 'АВ-3', 19))
# list_students.append(Student('Анетта', 'АВ-2', 18))
# list_students.append(Student('Василий', 'АВ-2', 18))
#
#
# list_students.sort(key=lambda x: len(x.name))
# # list_students.sort(key=lambda x: x.name)
# # list_students.sort(key=lambda x: x.age)
# # list_students.sort(key=lambda x: x.group)
#
# for student in list_students:
#     print('{}, {}, {}'.format(student.name, student.group, student.age))


# # В институте биоинформатики по офису передвигается робот. Недавно студенты из группы программистов написали
# # для него программу, по которой робот, когда видит программистов, считает их количество и произносит
# # вслух "n программистов".
# #
# # Для того, чтобы это звучало правильно, для каждого n нужно использовать верное окончание слова.
# #
# # Напишите программу, считывающую с пользовательского ввода целое число n (неотрицательное), выводящее
# # это число в консоль вместе с правильным образом изменённым словом "программист", для того, чтобы робот
# # мог нормально общаться с людьми, например: 1 программист, 2 программиста, 5 программистов.
#
# n = 101
#
# if n % 10 == 1 and n % 100 != 11:
#     end = ''
# elif (n % 100 != 12 and n % 100 != 13 and n % 100 != 14) and (n % 10 == 2 or n % 10 == 3 or n % 10 == 4):
#     end = 'а'
# else:
#     end = 'ов'
#
# print('%s программист%s' % (n, end))



# alp = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
# result = "Роскомнадзор запретил букву "
#
# # Перебор всех символов алфавита
# for c in alp:
#     # Проверяем, что в строке result текущая буква не найдена
#     if c in result or c.upper() in result:
#         # Выводим надпись
#         print(result + c.upper())
#
#         # Удаляем букву из надписи
#         result = result.replace(c, '')
#         result = result.replace(c.upper(), '')



# def parser_my_jira_time_logs(log):
#     """ Функция принимает список строк вида:
#     7417 10:00-12:00
#     7417 12:19-14:00
#     7417 14:37-15:30
#     7417 15:58-17:50
#
#     7415 15:58-15:59
#
#     7456 14:28-15:59
#
#     То, что перед ' ' -- уникальный номер задания
#     Диапазон после ' ' -- отрезок времени вида: начало - конец
#
#     Далее функция подсчитает количество часов и минут для каждого задания
#     и выведет их
#     """
#
#     # TODO: Защита от копипаста: строки могут повторяться и время подсчитается неправильно
#     # TODO: Если часы перевалят за 24, то начнется отсчет заного
#     # TODO: Для джиры дни и недели не астрономические: 1d = 8h и 1w = 5d
#
#     import re
#     pattern = re.compile(r'(.+) (\d\d:\d\d)-(\d\d:\d\d)')
#
#     from datetime import datetime as dt
#     import time
#     from collections import defaultdict
#
#     jira_time = defaultdict(int)
#
#     for line in log.split('\n'):
#         if line:
#             m = pattern.match(line.strip())
#
#             jira = m.group(1)
#             t1 = m.group(2)
#             t2 = m.group(3)
#             delta = dt.strptime(t2, '%H:%M') - dt.strptime(t1, '%H:%M')
#             seconds = delta.seconds
#
#             jira_time[jira] += seconds
#
#     for jira, secs in jira_time.items():
#         t = time.gmtime(secs)
#         h = t.tm_hour
#         m = t.tm_min
#         jira_time = None
#         if h:
#             jira_time = str(h) + 'h'
#         if m:
#             if jira_time:
#                 jira_time += ' ' + str(m) + 'm'
#             else:
#                 jira_time = str(m) + 'm'
#
#         print('%s: %s' % (jira, jira_time))
#
#
# parser_my_jira_time_logs("""
# 7417 10:00-12:00
# 7417 12:19-14:00
# 7417 14:37-15:30
# 7417 15:58-17:50
#
# 7415 15:58-15:59
#
# 7456 14:28-15:59
# """)


# def anonymization_quotes(quote_text):
#     """ Функция заменяет ники в цитатах на псевдонимы 'xxx', 'yyy' и т.п.
#     Шаблон определения "^(.+?):"
#
#     Пример валидной цитаты: "BlackFox: Кто нибудь, хоть раз, физически ощущал как он седеет?..."
#     """
#
#     import re
#     login_pattern = re.compile(r'^(.+?):')
#
#     # Словарь, в котором ключом является логин, а значением псевдоним
#     all_logins = {}
#
#     # Счетчик логинов
#     count_logins = 0
#
#     # Сгенерируем список с псевдонимами. Список будет вида: ['aaa', 'bbb', ..., 'zzz', 'AAA', ... 'ZZZ']
#     import string
#     login_aliases = [c*3 for c in string.ascii_letters]
#
#     # Разбиваем цитату по строчно
#     for line in quote_text.split('\n'):
#         # Ищем логин
#         match = login_pattern.search(line)
#
#         # Если нашли
#         if match:
#             # Вытаскиваем только логин -- нам не нужно двоеточние после логина
#             login = match.group(1)
#
#             # Если такого логина нет в словаре, добавляем в словарь логин и его псевдоним
#             if login not in all_logins:
#                 all_logins[login] = login_aliases[count_logins]
#                 count_logins += 1
#
#     quote = quote_text
#
#     # Проходим по словарю и делаем замену логина на псевдоним в строке цитаты
#     for login, alias in all_logins.items():
#         quote = quote.replace(login, alias)
#
#     return quote
#
#
# quote = """Аня: Не хочу и комп занят
# Кирилл: вредный старший брат окупировал комп?
# Кирилл: у моей сестры таже проблема"""
#
# print(quote)
#
# quote = anonymization_quotes(quote)
# print()
# print(quote)



# # TODO: пример работы с ini файлами
# # https://docs.python.org/3/library/configparser.html
#
# import configparser
#
# ini = configparser.ConfigParser()
# ini['Default'] = {
#     'x': 10,
#     'y': 15,
#     'z': 3,
# }
#
# ini['Additional'] = {}
# additional = ini['Additional']
# additional['top'] = str(True)
# additional['text'] = "Hello World!"
# additional['arrays'] = str([1, 2, 3, 4, 5])
#
# ini['Empty'] = {}
#
# with open('config.ini', 'w') as f:
#     ini.write(f)
#
#
# ini_read = configparser.ConfigParser()
# ini_read.read('config.ini')
# print(ini_read.sections())
#
# print(ini_read['Additional']['top'])
# print(ini_read['Additional']['text'])
# print(ini_read['Additional']['arrays'])
# print(ini_read['Additional']['arrays'].replace('[', '').replace(']', '').split(', '))
#
# import sys
# sys.exit()



# # Следующий пример строит график функции f(x) = x / sin(x):
#
# import math
#
# # !!! Импортируем один из пакетов Matplotlib
# import pylab
#
# # !!! Импортируем пакет со вспомогательными функциями
# from matplotlib import mlab
#
# if __name__ == '__main__':
#     # Будем рисовать график этой функции
#     def func(x):
#         """
#         sinc (x)
#         """
#         if x == 0:
#             return 1.0
#         return math.sin (x) / x
#
#     # Интервал изменения переменной по оси X
#     xmin = -20.0
#     xmax = 20.0
#
#     # Шаг между точками
#     dx = 0.01
#
#     # !!! Создадим список координат по оси X на отрезке [-xmin; xmax], включая концы
#     xlist = mlab.frange (xmin, xmax, dx)
#
#     # Вычислим значение функции в заданных точках
#     ylist = [func (x) for x in xlist]
#
#     # !!! Нарисуем одномерный график
#     pylab.plot (xlist, ylist)
#
#     # !!! Покажем окно с нарисованным графиком
#     pylab.show()



# left, right, up, down = 0, 0, 0, height
#
# # Перебор всех пикселей изображения
# for y in range(height):
#     for x in range(width):
#         # Получаем пиксель
#         pxl = im2.getpixel((x, y))
#
#         if pxl == black_pxl:
#             up = max(up, y)
#             down = min(down, y)
#
# print(left, right, up, down)






# # TODO: переместить в папку PySide
# ## Загрузка формы из файла ui
#
# # http://pyside.github.io/docs/pyside/index.html
# # http://visitusers.org/index.php?title=PySide_Recipes
#
#
# from PySide.QtGui import *
# from PySide.QtCore import *
# from PySide.QtSql import *
# from PySide.QtUiTools import *
#
# import sys
#
#
# app = QApplication(sys.argv)
#
# db = QSqlDatabase.addDatabase('QSQLITE')
# db.setDatabaseName('sqlite_test.bd')
# ok = db.open()
#
#
# model = QSqlTableModel()
# model.setTable('foo_table')
# model.setEditStrategy(QSqlTableModel.OnFieldChange)
# model.select()
#
#
# # Load the UI from a Qt designer file.
# loader = QUiLoader()
# file = QFile("mainwindow.ui")
# file.open(QFile.ReadOnly)
# mw = loader.load(file)
# file.close()
#
# mw.tableView.setModel(model)
# # mw.tableView.hideColumn(0)  # don't show the ID
#
# mw.show()
#
# app.exec_()



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
