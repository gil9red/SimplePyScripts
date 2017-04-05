#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'



quit()


import ctypes

# Drive types
DRIVE_UNKNOWN     = 0  # The drive type cannot be determined.
DRIVE_NO_ROOT_DIR = 1  # The root path is invalid; for example, there is no volume mounted at the specified path.
DRIVE_REMOVABLE   = 2  # The drive has removable media; for example, a floppy drive, thumb drive, or flash card reader.
DRIVE_FIXED       = 3  # The drive has fixed media; for example, a hard disk drive or flash drive.
DRIVE_REMOTE      = 4  # The drive is a remote (network) drive.
DRIVE_CDROM       = 5  # The drive is a CD-ROM drive.
DRIVE_RAMDISK     = 6  # The drive is a RAM disk.

# Map drive types to strings
DRIVE_TYPE_MAP = { DRIVE_UNKNOWN     : 'DRIVE_UNKNOWN',
                   DRIVE_NO_ROOT_DIR : 'DRIVE_NO_ROOT_DIR',
                   DRIVE_REMOVABLE   : 'DRIVE_REMOVABLE',
                   DRIVE_FIXED       : 'DRIVE_FIXED',
                   DRIVE_REMOTE      : 'DRIVE_REMOTE',
                   DRIVE_CDROM       : 'DRIVE_CDROM',
                   DRIVE_RAMDISK     : 'DRIVE_RAMDISK'}


# Return list of tuples mapping drive letters to drive types
def get_drive_info():
    result = []
    bitmask = ctypes.windll.kernel32.GetLogicalDrives()
    for i in range(26):
        bit = 2 ** i
        if bit & bitmask:
            drive_letter = '%s:' % chr(65 + i)
            drive_type = ctypes.windll.kernel32.GetDriveTypeA('%s\\' % drive_letter)
            result.append((drive_letter, drive_type))
    return result


# Test
if __name__ == '__main__':
    drive_info = get_drive_info()
    for drive_letter, drive_type in drive_info:
        print('%s = %s' % (drive_letter, DRIVE_TYPE_MAP[drive_type]))
    removable_drives = [drive_letter for drive_letter, drive_type in drive_info if drive_type == DRIVE_REMOVABLE]
    print('removable_drives = %r' % removable_drives)


quit()


# TODO: сделать программу, которая пишет список подключенных usb-устройств

# http://doc.qt.io/qt-5/qtserialport-terminal-example.html

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSerialPort import *


app = QApplication([])

for info in QSerialPortInfo.availablePorts():
    print("Name:", info.portName())
    print("Description:", info.description())
    print("Manufacturer:", info.manufacturer())


# # Example use QSerialPortInfo
# foreach (const QSerialPortInfo &info, QSerialPortInfo::availablePorts()) {
#     qDebug() << "Name : " << info.portName();
#     qDebug() << "Description : " << info.description();
#     qDebug() << "Manufacturer: " << info.manufacturer();
#
#     // Example use QSerialPort
#     QSerialPort serial;
#     serial.setPort(info);
#     if (serial.open(QIODevice::ReadWrite))
#         serial.close();
# }

# app.exec()


quit()


import win32com.client

wmi = win32com.client.GetObject("winmgmts:")
for i, usb in enumerate(wmi.InstancesOf("Win32_USBHub"), 1):
    print(i, usb.DeviceID)
quit()



quit()


# post_data = """
# <REQUEST OBJECT_CLASS="TAbonentObject" ACTION="GET_CHANGES" POINT_CODE=""
# VERSION="" TYPE_VERSION="" PORTION="" PACK="" BOOK_ID=""/>
# """
#
# post_data = """
#
# <REQUEST OBJECT_CLASS="TAbonentObject" ACTION="GET_CHANGES" POINT_CODE="TZCL" TYPE_VERSION="I" VERSION="261672" />
# """
#
# post_data = """
# <?xml version="1.0" encoding="windows-1251"?>
# <REQUEST OBJECT_CLASS="TAbonentObject" ACTION="GET_CHANGES" POINT_CODE="TZGX" VERSION="0" TYPE_VERSION="I" PORTION="1" PACK="ZLIB" PART="0"/>
# """
#
# post_data = """
# <REQUEST OBJECT_CLASS="TAbonentObject" ACTION="GET_CHANGES" POINT_CODE="CDPA" TYPE_VERSION="I" VERSION="0"
# INT_SOFT_ID="CCD38CEB-58A8-4D26-9859-706FE1497F86"
# />
# """
#
# post_data = """
# <?xml version="1.0" encoding="UTF-8"?>
# <REQUEST OBJECT_CLASS="TAbonentObject" ACTION="Ping" POINT_CODE="TZUM" USER_ID="1" INT_SOFT_ID="DA61D1CE-757F-44C3-B3F7-11A026C37CD4"/>
# """
#
# import requests
# rs = requests.post('http://10.7.8.31:12000', data=post_data)
# print(rs)
# print(rs.content)
# print(rs.content.decode('cp1251'))


import requests
# rs = requests.get('https://enter.contact-sys.com:2221/wstrans/wsTrans.exe/soap/ITransmitter')
# rs = requests.get('http://0.0.0.0:12000')
# rs = requests.get('http://10.7.8.31:12000')

post_data = """
<REQUEST OBJECT_CLASS="TAbonentObject" ACTION="GET_CHANGES" POINT_CODE=""
VERSION="" TYPE_VERSION="" PORTION="" PACK="" BOOK_ID=""/>
"""

post_data = """

<REQUEST OBJECT_CLASS="TAbonentObject" ACTION="GET_CHANGES" POINT_CODE="TZCL" TYPE_VERSION="I" VERSION="261672" />
"""

post_data = """
<?xml version="1.0" encoding="windows-1251"?>
<REQUEST OBJECT_CLASS="TAbonentObject" ACTION="GET_CHANGES" POINT_CODE="TZGX" VERSION="0" TYPE_VERSION="I" PORTION="1" PACK="ZLIB" PART="0"/>
"""
rs = requests.post('http://10.7.8.31:12000', data=post_data)
# rs = requests.post('http://0.0.0.0:12000', data=post_data)
print(rs)
print(rs.content.decode('cp1251'))

# 10.7.8.31:12000

quit()

json_rows = list()

import csv
with open('_.csv', newline='', encoding='utf-8') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';')

    csv_rows = list(spamreader)
    headers = csv_rows[0]

    # ['Card', 'PAN', 'PSNTag 5F34', 'Expiry', 'Country', 'Currency', 'Product', 'Magstripe',
    # 'VSDCCVN', 'qVSDC CVN', 'MSD', 'Comments', 'BIN', 'Track 2 data', 'Track 1 data',
    # 'CVV2', 'PIN']
    # print(headers)

    # Словарь для поиска повторяющихся переменных, например PAN и Expiry у многих
    # повторяется.
    # Ключом словаря будет кортеж (<название_переменной>, <значение>) и счетчика
    # совпадений. Уникальным значение будет 1
    params_group_dict = dict()

    pan_list = list()

    for rows in csv_rows[1:]:
        if rows[1] in pan_list:
            print(rows)
            continue

        pan_list.append(rows[1])

        from collections import OrderedDict
        row_data = OrderedDict()

        # PAN, BIN, Expiry, Track_2_data, Track_1_data, CVV2, PIN
        #
        # 0     1    2            3       4        5         6        7          8
        # Card, PAN, PSNTag 5F34, Expiry, Country, Currency, Product, Magstripe, VSDCCVN,
        #
        # 9          10   11        12   13            14            15    16
        # qVSDC CVN, MSD, Comments, BIN, Track 2 data, Track 1 data, CVV2, PIN
        row_data['Number'] = rows[0]
        row_data['PAN'] = rows[1]
        row_data['BIN'] = rows[12]
        row_data['Expiry'] = rows[3]
        row_data['Track_2_data'] = rows[13]
        row_data['Track_1_data'] = rows[14]
        row_data['CVV2'] = rows[15]
        row_data['PIN'] = rows[16]

        for k, v in row_data.items():
            if (k, v) not in params_group_dict:
                params_group_dict[(k, v)] = 0

            params_group_dict[(k, v)] += 1

        # # print(rows)
        # for field_name, value in zip(headers, rows):
        #     row_data[field_name] = value

        json_rows.append(row_data)


params_group_dict_filtered = dict(filter(lambda x: x[1] > 1, params_group_dict.items()))
# print(params_group_dict_filtered)

from collections import defaultdict
params_by_values_dict = defaultdict(list)
for k, _ in params_group_dict_filtered.items():
    params_by_values_dict[k[0]].append(k[1])

var_by_params_dict = dict()
for k, values in params_by_values_dict.items():
    for i, v in enumerate(values, 1):
        global_var = '<TestCard_Group_{}_{}>'.format(k, i)
        var_by_params_dict[v] = global_var

# for k, v in var_by_params_dict.items():
#     print('{}: {}'.format(v, k))

variable_pattern = 'TestCard_{}_{}'

from collections import OrderedDict
variables_dict = OrderedDict()

# Аналог variables_dict, но с заменой повторяющихся переменных
# общими
variables_dict_shorted = OrderedDict()
variables_dict_shorted = OrderedDict()
global_variables_dict_shorted = OrderedDict()


for data in json_rows:
    # print(data)

    for k, v in data.items():
        if k != 'Number':
            var = variable_pattern.format(data['Number'], k)
            variables_dict[var] = v

            variables_dict_shorted[var] = v
            if v in var_by_params_dict:
                global_variables_dict_shorted[var_by_params_dict[v]] = v
                variables_dict_shorted[var] = var_by_params_dict[v], v

print()
# print(len(variables_dict))
# for k, v in variables_dict.items():
#     print('{}: {}'.format(k, v))
print(len(variables_dict))
print(len(list(filter(lambda x: not isinstance(x[1], tuple), variables_dict_shorted.items()))))
print(len(global_variables_dict_shorted))

pans = list()
for k, v in variables_dict_shorted.items():
    if 'PAN' in k:
        pans.append(v)

print(len(pans))
print(len(set(pans)))

# quit()

# print()
# i = 0
# for k, v in variables_dict_shorted.items():
#     # if isinstance(v, tuple):
#     #     continue
#
#     # print('{}: {}'.format(k, v))
#     print('{}\t{}'.format(k, v[0] if isinstance(v, tuple) else v))
#
#     i += 1
#     if i % 7 == 0:
#         print()
#
# print()
# print()
# for k, v in sorted(global_variables_dict_shorted.items(), key=lambda x: x[0]):
#     print('{}\t{}'.format(k, v))


# TODO: еще хорошо бы и тип указывать в TestParameter
# TODO: некоторые из значений -- "N/A", а это наверное не по стандарту, возможно это нужно заменять пустой строкой
TestParameter_pattern = '<tes:TestParameter Name="{}"><tes:Kind>0</tes:Kind></tes:TestParameter>'
TestParameterValue_pattern = '<tes:TestParameterValue TestParameterName="{}"><tes:Value>{}</tes:Value></tes:TestParameterValue>'

xml_pattern = '''<?xml version="1.0" encoding="UTF-8"?>
<tes:TestParameterGroups xmlns:tes="http://schemas.optt.com/testSetupImpExp.xsd">
  <tes:TestParameterGroup ExtGuid="HEAK6HV6CBDC5LRIJ6UIN7FRTY">
    <tes:Title>Visa Test Card</tes:Title>
    <tes:TestParameters>
      {}
    </tes:TestParameters>
    <tes:TestParameterValueSets>
      <tes:TestParameterValueSet ExtGuid="EHJRPDW54NCTXHGR2FW6YNDQYQ">
        <tes:Title>Test cards</tes:Title>
        <tes:TestParameterValues>
          {}
        </tes:TestParameterValues>
      </tes:TestParameterValueSet>
    </tes:TestParameterValueSets>
  </tes:TestParameterGroup>
</tes:TestParameterGroups>
'''

TestParameter_list = list()
TestParameterValue_list = list()

all_vars = list()
all_vars += [(var[1: -1], k) for var, k in global_variables_dict_shorted.items()]
all_vars += list(filter(lambda x: not isinstance(x[1], tuple), variables_dict_shorted.items()))
for k, v in all_vars:
    print(k, v)
    TestParameter_list.append(TestParameter_pattern.format(k))
    TestParameterValue_list.append(TestParameterValue_pattern.format(k, v))

xml = xml_pattern.format(''.join(TestParameter_list), ''.join(TestParameterValue_list))
print(xml)
open('test_params_group_for_visa_test_cards.xml', 'w', encoding='utf-8').write(xml)


from bs4 import BeautifulSoup
BeautifulSoup(open('test_params_group_for_visa_test_cards.xml'), 'lxml')

# for k, v in sorted(filter(lambda x: x[1] > 1, params_group_dict.items()), key=lambda x: x[0]):
#     print(k, v)

# import json
# print(json.dumps(json_rows, ensure_ascii=False, indent=4).replace('"', "'"))


quit()

# json_rows = list()
#
# import csv
# with open('_.csv', newline='', encoding='utf-8') as csvfile:
#     spamreader = csv.reader(csvfile, delimiter=';')
#
#     csv_rows = list(spamreader)
#     headers = csv_rows[0]
#
#     print(headers)
#
#     for rows in csv_rows[1:]:
#         from collections import OrderedDict
#         row_data = OrderedDict()
#
#         # print(rows)
#         for field_name, value in zip(headers, rows):
#             row_data[field_name] = value
#
#         json_rows.append(row_data)
#
#
# import json
# print(json.dumps(json_rows, ensure_ascii=False).replace('"', "'"))


quit()


api_key = None
url = 'https://search-maps.yandex.ru/v1/?text=Магнитогорск, бизнец-центра&type=biz&lang=ru_RU&apikey={}'.format(api_key)
import requests
print(requests.get(url).json())


quit()

# import PyPDF2
# pdf_file = open('test.pdf', 'rb')
# read_pdf = PyPDF2.PdfFileReader(pdf_file)
# number_of_pages = read_pdf.getNumPages()
# page = read_pdf.getPage(0)
# print(page)
# page_content = page.extractText()
# print(page_content)
# print(page_content.encode('utf-8'))
#
# quit()


import os
from flask import Flask, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
UPLOAD_FOLDER = os.path.abspath(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file:
            # Функция secure_filename не дружит с не ascii-символами, поэтому
            # файлы русскими словами не называть
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Функция url_for('uploaded_file', filename=filename) возвращает строку вида: /uploads/<filename>
            return redirect(url_for('uploaded_file', filename=filename))

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


# Пример обработчика, возвращающий файлы из папки app.config['UPLOAD_FOLDER'] для путей uploads и files.
# т.е. не нужно давать специальное название, чтобы получить файл в flask
@app.route('/uploads/<filename>')
@app.route('/files/<filename>')
def uploaded_file(filename):
    # NOTE: не работает
    # print(filename)
    # if os.path.isdir(filename):
    #     parts = filename.split('/')
    #     filename = parts[-1]
    #
    #     # Возврат списка с первого до предпоследнего элемента (у нас это имя файла) и распаковывание списка
    #     my_dir = os.path.join(app.config['UPLOAD_FOLDER'], *parts[:-1])
    #     print(my_dir)
    #
    #     return send_from_directory(my_dir, filename)
    # else:
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# Localhost
app.run()


# from sqlalchemy import create_engine, inspect
#
# engine = create_engine("postgresql+psycopg2://localhost/test")
# insp = inspect(engine)  # will be a PGInspector
#
# print(insp.get_enums())


quit()


"""Скрипт для эмуляции запроса поиска видео в vk"""


LOGIN = '<LOGIN>'
PASSWORD = '<PASSWORD>'

if __name__ == '__main__':
    import requests
    session = requests.Session()
    session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'

    rs = session.get('https://m.vk.com')

    import re
    match = re.search(r'<form method="post" action="(.+?)"', rs.text)

    # Авторизация. По полученной ссылке делаем post запрос с данными формы -- логин и пароль
    url = match.group(1)
    url = url + '&email=' + LOGIN + '&pass=' + PASSWORD
    rs = session.post(url)

    rs = session.post('https://vk.com/al_video.php?act=search_video&al=1&offset=0', data={'q': 'Варкрафт 2016'})
    print(rs)
    json_text = rs.text
    print(json_text)

    start = json_text.index('{')
    end = json_text.rindex('}')
    json_text = json_text[start:end + 1]
    print(json_text)
    import json
    data = json.loads(json_text)
    print(data)

    print()
    print('Result:')

    import requests
    import re

    def get_video_file_urls(url):
        video_urls = list()

        rs = session.get(url)
        if not rs.ok:
            print(rs)
            return video_urls

        for source in re.findall(r'<source.+?>', rs.text):
            source = source.replace('\\', '')
            match = re.search('src="(http.+?\.mp4).*?"', source)
            if match:
                url_video = match.group(1)
                video_urls.append(url_video)

        return video_urls


    for video_data in data['list']:
        print(video_data)
        owner = video_data[0]
        video_id = video_data[1]
        poster = video_data[2]
        title = video_data[3]

        # TODO: для мобильной ссылки работает поиск, однако качество всегдла -- 240
        # нужно научить парсер искать ссылки в другом формате, текущий -- через тег source работает
        video_url = 'https://m.vk.com/video{}_{}'.format(owner, video_id)
        print(title, video_url)
        for file_url in get_video_file_urls(video_url):
            print('    {}'.format(file_url))
        print()


quit()


# TODO: использовать http://www.cbr.ru/scripts/Root.asp?PrtId=SXML или разобраться с данными от query.yahooapis.com
# непонятны некоторые параметры
# TODO: сделать консоль
# TODO: сделать гуй
# TODO: сделать сервер
import requests

rs = requests.get('https://query.yahooapis.com/v1/public/yql?q=select+*+from+yahoo.finance.xchange+where+pair+=+%22USDRUB,EURRUB%22&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback=')
print(rs.json())

for rate in rs.json()['query']['results']['rate']:
    print(rate['Name'], rate['Rate'])


quit()


# from winreg import OpenKey, EnumValue, HKEY_CURRENT_USER, KEY_READ
#
#
# def get_key_value(key, key_key):
#
#     i = 0
#     while True:
#         try:
#             k, v, _ = EnumValue(key, i)
#             if k == key_key:
#                 return v
#             i += 1
#
#         except WindowsError:
#             break
#
# key = OpenKey(HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\Shell\\Bags\\1\\Desktop", 0, KEY_READ)
# print(get_key_value(key, 'ItemPos1920x1080x96(1)'))
#
# quit()


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


# import goslate
# gs = goslate.Goslate()
# print('\n', gs.translate(r, 'ru'))
#
# # from translate import Translator
# # translator = Translator(to_lang="ru")
# # translation = translator.translate(r)
# # print(translation)


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


# TODO: service parse.com
# https://parse.com
# https://parse.com/docs/api_libraries
# https://github.com/dgrtwo/ParsePy
# http://habrahabr.ru/post/246989/


# TODO: больше примеров работы с модулями py
# http://pythonworld.ru/karta-sajta


# TODO: придумать простое приложение и реализовтаь его с помощью TDD (используя unit-тесты)


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
