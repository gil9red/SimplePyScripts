#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


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

#
#
# # https://good-developers.com/prostoj-telegram-bot/#comment-5427
#
# # -*- coding: utf-8 -*-
# #
# #
# # Импортировать модули телеграма
# from telegram import Updater, Emoji, ParseMode
# import telegram
# from time import sleep
# #
# import logging
# import requests, json
# import urllib.request, urllib.parse, urllib
# import urllib.request
# import re, sys, os, platform
# import random  as  random_number
#
# #
# # Переменные и Запросы
# help_text = 'Текст, который будет выводиться при команде /help'
# #
# # Юзер новый заходит в чат
# welcome_text = 'Текст, который будет выводиться, когда юзер заходит в чат'
# #
# # Юзер покидает чат
# goodbuy_text = 'Текст, который будет выводиться, когда юзер выходит из чата'
# #
# # Локальный IP адрес
# MY_IP = '1.2.3.4'
# # Будет такой себе переключатель. Когда True - обрабатывать сообщения
# # Когда False - не принимать сообщения
# WORK = True
# # ID чата админа и его Username
# ADMIN_CHAT = '1234567'
# ADMIN_USERNAME = "@username"
# # Адрес хранения мультимедиа
# IMG_URI = 'https://vsbot.good-developers.com/'
# #
# # Логирование
# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO)
# logger = logging.getLogger(__name__)
#
#
# #
# #
#
# # Отправка сообщения на команду /help
# def help(bot, update):
#     bot.sendMessage(update.message.chat_id, text=help_text, parse_mode=ParseMode.MARKDOWN)
# # Отправка ошибки в чат админу
# def error(bot, update, error):
#     bot.sendMessage(ADMIN_CHAT, text=error, parse_mode=ParseMode.MARKDOWN)
# # Отправка сообщения на команду /start
# def start(bot, update):
#     bot.sendMessage(chat_id=update.message.chat_id, text="Привет! Набери /help и получишь список команд.")
# #
# #
# # Поиск на YouTube
# def video(bot, update,msg):
#     link = urllib.parse.urlencode({"search_query" : msg})
#     content = urllib.request.urlopen("https://www.youtube.com/results?" + link)
#     search_results = re.findall('href=\"\/watch\?v=(.*?)\"', content.read().decode())
#     if len(search_results)>0:
#         # Первые 10 результатов
#         search_results = search_results[0:9:1]
#         choice_f = random_number.choice(search_results)
#         yt_link = "https://www.youtube.com/watch?v="+choice_f
#         bot.sendMessage(update.message.chat_id, text=yt_link, parse_mode=ParseMode.MARKDOWN)
#     else:
#         bot.sendMessage(update.message.chat_id, text='Ничего не найдено.')
# #
# # Поиск Картинки на Яндексе
# def pic(bot, update, msg):
#     ss = requests.Session()
#     r = ss.get('https://yandex.ua/images/search?text='+msg)
#     p = 'div.class\=\"serp-item.*?url\"\:\"(.*?)\"'
#     response = r.text
#     w = re.findall(p,response)
#     #
#     if len(w)>0:
#         # Первые 30 фото
#         w = w[0:29:1]
#         choice_f = random_number.choice(w)
#         bot.sendPhoto(update.message.chat_id, photo=choice_f)
#     else:
#         bot.sendMessage(update.message.chat_id, 'Ничего не найдено')
# #
# # Получить первую ссылку
# def g(bot, update, msg):
#     f = { 'v' : '1.0', 'q' : msg, 'userip' : MY_IP}
#     g_search = urllib.parse.urlencode(f)
#     s = requests.Session()
#     url = ('https://ajax.googleapis.com/ajax/services/search/web?'+g_search)
#     r = s.get(url,cookies={'my': 'browser'})
#     response = r.text
#     #
#     pattern = '\"GwebSearch\","unescapedUrl\"\:\"(.*?)\"'
#     g_search = re.findall(pattern,response)
#     if len(g_search)>0:
#         g_search = g_search[0]
#         g_search = g_search.replace('\\u0026','&amp;')
#         g_search = g_search.replace('\\u003d','=')
#         bot.sendMessage(update.message.chat_id, text=g_search, parse_mode=ParseMode.MARKDOWN)
#     else:
#         bot.sendMessage(update.message.chat_id, text='Ничего не найдено.')
# #
# #
# # Обработка команд!
# def do_it(bot, update):
#     msg = update.message.text
#     global WORK
#     if len(msg)>130:
#         txt = 'Превышено ограничение в *130* символов для команды. ' \
#               'Тут не *130*, а *'+str(len(msg))+'*!'
#         bot.sendMessage(update.message.chat_id, text=txt, parse_mode=ParseMode.MARKDOWN)
#         msg = ''
#     # Поиск в Google
#     cmd = ''
#     pattern = '^!g (.*?)$'
#     cmd = re.findall(pattern,msg)
#     if len(cmd)>0:
#         g(bot,update,cmd[0])
#     # Поиск Картинки в Яндекс
#     cmd = ''
#     pattern = '^!pic (.*?)$'
#     cmd = re.findall(pattern,msg)
#     if len(cmd)>0:
#         pic(bot,update,cmd[0])
#     # Поиск видео на Yooutube
#     cmd = ''
#     pattern = '^!yt (.*?)$'
#     cmd = re.findall(pattern,msg)
#     if len(cmd)>0:
#         video(bot,update,cmd[0])
#     # Выключить бот
#     cmd = ''
#     pattern = '^!тихо$'
#     cmd = re.findall(pattern,msg)
#     if len(cmd)>0:
#         WORK = False
#         txt = 'Я ухожу. Напишите *'+ADMIN_USERNAME+'* что бы я вернулся.'
#         bot.sendMessage(update.message.chat_id, text=txt, parse_mode=ParseMode.MARKDOWN)
# #
# # Анализ текста
# def analyse_text(bot, update, words):
#     msg = update.message.text
#     # Перевод в нижний регистр
#     msg = msg.lower()
#     # Небольшой словарь
#     a3 = ["привет бот","привет всем", "всем привет"]
#     q3 = "Привет человек"
#     #
#     C_DIC = {q1:a1}
#     # Считаем стандартные фразы
#     for a, b in C_DIC.items():
#         for c in b:
#             if c in msg:
#                 # Типа бот печатает и сейчас ответит
#                 bot.sendChatAction(update.message.chat_id, action=telegram.ChatAction.TYPING)
#                 sleep(2)
#                 #ans = random_number.choice(a)
#                 bot.sendMessage(update.message.chat_id, text=a, parse_mode=ParseMode.MARKDOWN)
# #
# # Предварительный анализ сообщения
# def think(bot, update):
#     msg = update.message.text
#     # Перевод в нижний регистр
#     msg = msg.lower()
#     # Количество слов узнаем
#     p = '([a-zA-Zа-яА-Я]+)'
#     words = re.findall(p,msg)
#     msg_count = len(words)
#     # Много наговорил
#     if msg_count> 100:
#         txt = 'Много написал, не понимаю!'
#         bot.sendMessage(update.message.chat_id, text=txt, parse_mode=ParseMode.MARKDOWN)
#     # Слишком много наговорил
#     if msg_count>400:
#         lnk = IMG_URI+'53L3fx6EJ7Fl9UiEzDRC.png'
#         bot.sendPhoto(update.message.chat_id, photo=lnk)
#     # Короткий текст
#     if msg_count<100:
#         analyse_text(bot, update, words)
# #
# # Обработка сообщения
# def echo(bot, update):
#     cid = update.message.chat_id
#     # Проверка блокировки
#     #print(update.message.text)
#     global WORK
#     global ADMIN_CHAT
#     if WORK==False:
#         if str(cid) != ADMIN_CHAT:
#             update.message.text = ''
#         else:
#             # Ищем команду запуска
#             cmd = ''
#             pattern = '^!работай$'
#             cmd = re.findall(pattern,update.message.text)
#             if len(cmd)>0:
#                 WORK = True
#                 txt_r = 'Вернусь к работе!'
#                 bot.sendMessage(update.message.chat_id,
#                                 text=txt_r,
#                                 parse_mode=ParseMode.MARKDOWN)
#     #
#     msg = update.message.text
#     # Новый или вышел
#     if (update.message.new_chat_participant)!=None:
#         bot.sendMessage(update.message.chat_id, text=welcome_text, parse_mode=ParseMode.MARKDOWN)
#     if (update.message.left_chat_participant)!=None:
#         bot.sendMessage(update.message.chat_id, text=goodbuy_text, parse_mode=ParseMode.MARKDOWN)
#     # Проверяем поступила ли прямая команда
#     cmd = ''
#     pattern = '^!(.*?)$'
#     cmd = re.findall(pattern,msg)
#     if len(cmd)>0:
#         do_it(bot, update)
#     else:
#         think(bot, update)
# #
#
#
# #
# def main():
#     # Создаем класс Updater и указываем текущий токен вашего бота
#     updater = Updater("ТОКЕН")
#     dp = updater.dispatcher
#     # Задаем стандартные команды /help /start. Они должны быть установлены по умолчанию.
#     dp.addTelegramCommandHandler("start", start)
#     dp.addTelegramCommandHandler("help", help)
#     dp.addTelegramMessageHandler(echo)
#     # Добавляем обработку ошибок. Они будут записываться в функции error
#     dp.addErrorHandler(error)
#     # Запускаем
#     updater.start_polling()
#     updater.idle()
# #
# if __name__ == '__main__':
#     main()
# #
#
# quit()

TOKEN = '<TOKEN>'


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')


def echo(bot, update):
    bot.sendMessage(update.message.chat_id, text=update.message.text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


# TODO: правильное название функции
def curs(bot, update):
    import requests

    rs = requests.get('https://query.yahooapis.com/v1/public/yql?q=select+*+from+yahoo.finance.xchange+where+pair+=+%22USDRUB,EURRUB%22&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback=')

    text = 'Курс:'
    for rate in rs.json()['query']['results']['rate']:
        text += '\n' + rate['Name'].split('/')[0] + ' ' + rate['Rate']

    print(text)
    bot.sendMessage(update.message.chat_id, text=text)


def pict(bot, update):
    bot.sendPhoto(update.message.chat_id, 'http://e3.postfact.ru/auto/18/91/16/OP_836_page01.png')


def pict2(bot, update):
    with open('OP_836_page02.png', 'rb') as f:
        bot.sendPhoto(update.message.chat_id, f)


#
#
# Поиск на YouTube
def video(bot, update, args):
    print(args)
    if not args:
        bot.sendMessage(update.message.chat_id, text='К команде добавьте запрос.')
        return

    msg = ' '.join(args)

    import urllib
    import re
    import random
    from telegram import ParseMode

    link = urllib.parse.urlencode({"search_query": msg})
    content = urllib.request.urlopen("https://www.youtube.com/results?" + link)
    search_results = re.findall('href=\"\/watch\?v=(.*?)\"', content.read().decode())
    if len(search_results)>0:
        # Первые 10 результатов
        search_results = search_results[0:9:1]
        choice_f = random.choice(search_results)
        yt_link = "https://www.youtube.com/watch?v="+choice_f
        bot.sendMessage(update.message.chat_id, text=yt_link, parse_mode=ParseMode.MARKDOWN)
    else:
        bot.sendMessage(update.message.chat_id, text='Ничего не найдено.')


locale = 'ru-RU'
gender = 'female'


# TODO:
def speak(bot, update, args):
    print(args)

    if not args:
        # # TODO: писать об ошиюке в чат
        # print('Список пуст')
        # return
        args = ['Сорок тысяч обезьян в жопу сунули банан']

    def bing_speak(text, locale, gender):
        """
        Функция выполняет запрос в bing сервис синтезирования речи и возвращает получившийся mp3-файл с речью
        в виде байтовой строки.

        """

        # Примеры запросов в сервис синтезирования речи:
        # http://www.bing.com/translator/api/language/Speak?locale=ru-RU&gender=male&media=audio/mp3&text=gil9red+%D0%BA%D0%BB%D0%B5%D0%B2%D1%8B%D0%B9+%D1%87%D1%83%D0%B2%D0%B0%D0%BA
        # http://www.bing.com/translator/api/language/Speak?locale=ru-RU&gender=female&media=audio/mp3&text=gil9red+%D0%BA%D0%BB%D0%B5%D0%B2%D1%8B%D0%B9+%D1%87%D1%83%D0%B2%D0%B0%D0%BA

        url = 'http://www.bing.com/translator/api/language/Speak'
        params = {
            'locale': locale,
            'gender': gender,
            'media': 'audio/mp3',
            'text': text,
        }

        import requests
        s = requests.Session()

        # Получим куки, иначе получим ошибку: {"message": "Service unavailable. Please try again later."}
        rs = s.get('http://www.bing.com/translator')
        if not rs.ok:
            raise Exception('Error [%s]: %s.', rs.status_code, rs.text)

        rs = s.get(url, params=params)
        if not rs.ok:
            raise Exception('Error [%s]: %s.', rs.status_code, rs.text)

        return rs.content

    # with open('OP_836_page02.png', 'rb') as f:

    # Первый элемент args -- текст
    # Второй голос
    # Третий локаль
    #
    text = ' '.join(args)
    mp3_content = bing_speak(text, locale, gender)

    # TODO: выглядит костыльно
    # Сохраняем в файл и возвращаем объект для считывания
    with open('speak.mp3', 'wb') as f:
        f.write(mp3_content)

        with open('speak.mp3', 'rb') as f:
            bot.sendAudio(update.message.chat_id, audio=f, title='Speak {} {}'.format(gender, locale))


def speak_set_locale(bot, update, args):
    print('speak_set_locale')
    if not args:
        # TODO: писать об ошиюке в чат
        print('Список пуст')
        return

    global locale
    last_locale = locale
    locale = args[0]

    bot.sendMessage(update.message.chat_id, text='Speak locale изменена: {} -> {}.'.format(last_locale, locale))


def speak_set_gender(bot, update, args):
    print('speak_set_gender')
    if not args:
        # TODO: писать об ошиюке в чат
        print('Список пуст')
        return

    global gender
    last_gender = gender
    gender = args[0]

    bot.sendMessage(update.message.chat_id, text='Speak gender изменена: {} -> {}.'.format(last_gender, gender))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("HI", lambda bot, update: bot.sendMessage(update.message.chat_id, text='HIII!')))
    dp.add_handler(CommandHandler("hi", lambda bot, update: bot.sendMessage(update.message.chat_id, text='hi')))
    dp.add_handler(CommandHandler("say", lambda bot, update, args: bot.sendMessage(update.message.chat_id, text='I say: "{}".'.format(args)), pass_args=True))
    dp.add_handler(CommandHandler("curs", curs))
    dp.add_handler(CommandHandler("pict", pict))
    dp.add_handler(CommandHandler("pict2", pict2))
    dp.add_handler(CommandHandler("yt", video, pass_args=True))

    dp.add_handler(CommandHandler("speak", speak, pass_args=True))
    dp.add_handler(CommandHandler("speak_set_locale", speak_set_locale, pass_args=True))
    dp.add_handler(CommandHandler("speak_set_gender", speak_set_gender, pass_args=True))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler([Filters.text], echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

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


import win32com.client

wmi = win32com.client.GetObject("winmgmts:")
for i, usb in enumerate(wmi.InstancesOf("Win32_USBHub"), 1):
    print(i, usb.DeviceID)
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


# NOTE: set position icon
# SOURCE: http://webcache.googleusercontent.com/search?q=cache:GoDfFADI1_oJ:systools.losthost.org/%3Fcode%3D9+&cd=15&hl=ru&ct=clnk&client=firefox-b-ab
# SendMessage(lv, LVM_SETITEMPOSITION, i, MAKELONG(pt.x, pt.y));



import ctypes


def GetDesktopListViewHandle():
    """
    Функция возвращает указатель на ListView рабочего стола.

    Оригинал:
    function GetDesktopListViewHandle: THandle;
        var
            S: string;
        begin
            Result := FindWindow('ProgMan', nil);
            Result := GetWindow(Result, GW_CHILD);
            Result := GetWindow(Result, GW_CHILD);
            SetLength(S, 40);
            GetClassName(Result, PChar(S), 39);
            if PChar(S) <> 'SysListView32' then
                Result := 0;
        end;

    """

    import ctypes
    FindWindow = ctypes.windll.user32.FindWindowW
    GetWindow = ctypes.windll.user32.GetWindow

    def GetClassName(hwnd):
        buff = ctypes.create_unicode_buffer(100)
        ctypes.windll.user32.GetClassNameW(hwnd, buff, 99)
        return buff.value

    from win32con import GW_CHILD

    # Ищем окно с классом "Progman" ("Program Manager")
    hwnd = FindWindow('Progman', None)
    hwnd = GetWindow(hwnd, GW_CHILD)  # SHELLDLL_DefView
    hwnd = GetWindow(hwnd, GW_CHILD)  # SysListView32

    if GetClassName(hwnd) != 'SysListView32':
        return 0

    return hwnd


def ListView_GetItemCount(hwnd):
    """

    Функция возвращает количество элементов указанного ListView.

    Оригинал:
    define ListView_GetItemCount(hwnd) (int)SNDMSG((hwnd),LVM_GETITEMCOUNT,(WPARAM)0,(LPARAM)0)

    """

    import commctrl
    import ctypes
    SendMessage = ctypes.windll.user32.SendMessageW

    return SendMessage(hwnd, commctrl.LVM_GETITEMCOUNT, 0, 0)


class LVITEMW(ctypes.Structure):
    _fields_ = [
        ('mask', ctypes.c_uint32),
        ('iItem', ctypes.c_int32),
        ('iSubItem', ctypes.c_int32),
        ('state', ctypes.c_uint32),
        ('stateMask', ctypes.c_uint32),
        ('pszText', ctypes.c_uint64),
        ('cchTextMax', ctypes.c_int32),
        ('iImage', ctypes.c_int32),
        ('lParam', ctypes.c_uint64),  # On 32 bit should be c_long
        ('iIndent', ctypes.c_int32),
        ('iGroupId', ctypes.c_int32),
        ('cColumns', ctypes.c_uint32),
        ('puColumns', ctypes.c_uint64),
        ('piColFmt', ctypes.c_int64),
        ('iGroup', ctypes.c_int32),
    ]


# def get_desktop_icons_list():
#     import struct
#     import ctypes
#     from commctrl import LVIF_TEXT, LVIF_IMAGE, LVM_GETITEMTEXT, LVM_GETITEMPOSITION, LVIR_BOUNDS, LVM_GETITEMRECT, LVM_GETITEMW
#     from win32con import PROCESS_ALL_ACCESS, MEM_RESERVE, MEM_COMMIT, PAGE_READWRITE, MEM_RELEASE
#     from ctypes.wintypes import POINT, RECT
#
#     GetWindowThreadProcessId = ctypes.windll.user32.GetWindowThreadProcessId
#     SendMessage = ctypes.windll.user32.SendMessageW
#     OpenProcess = ctypes.windll.kernel32.OpenProcess
#     VirtualAllocEx = ctypes.windll.kernel32.VirtualAllocEx
#     WriteProcessMemory = ctypes.windll.kernel32.WriteProcessMemory
#     ReadProcessMemory = ctypes.windll.kernel32.ReadProcessMemory
#     VirtualFreeEx = ctypes.windll.kernel32.VirtualFreeEx
#     CloseHandle = ctypes.windll.kernel32.CloseHandle
#
#     MAX_LEN = 4096
#
#     icons_list = list()
#
#     try:
#         hwnd = GetDesktopListViewHandle()
#         pid = ctypes.create_string_buffer(4)
#         p_pid = ctypes.addressof(pid)
#         GetWindowThreadProcessId(hwnd, p_pid)
#
#         h_process = OpenProcess(PROCESS_ALL_ACCESS, False, struct.unpack("i", pid)[0])
#         buffer_txt = VirtualAllocEx(h_process, 0, MAX_LEN, MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE)
#
#         copied = ctypes.create_string_buffer(4)
#         p_copied = ctypes.addressof(copied)
#
#         lvitem = LVITEMW()
#         lvitem.mask = ctypes.c_uint32(LVIF_TEXT | LVIF_IMAGE)
#         lvitem.iItem = ctypes.c_int32(0)
#         lvitem.iSubItem = ctypes.c_int32(0)
#         lvitem.pszText = ctypes.c_uint64(buffer_txt)
#         lvitem.cchTextMax = ctypes.c_int32(MAX_LEN)
#
#         p_buffer_lvi = VirtualAllocEx(h_process, 0, MAX_LEN, MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE)
#         WriteProcessMemory(h_process, p_buffer_lvi, ctypes.addressof(lvitem), ctypes.sizeof(LVITEMW), p_copied)
#
#         p_buffer_point = VirtualAllocEx(h_process, 0, ctypes.sizeof(POINT), MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE)
#         p_buffer_rect = VirtualAllocEx(h_process, 0, ctypes.sizeof(RECT), MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE)
#
#         num_items = ListView_GetItemCount(hwnd)
#
#         for i in range(num_items):
#             # Get icon text
#             SendMessage(hwnd, LVM_GETITEMTEXT, i, p_buffer_lvi)
#             target_bufftxt = ctypes.create_string_buffer(MAX_LEN)
#             ReadProcessMemory(h_process, buffer_txt, ctypes.addressof(target_bufftxt), MAX_LEN, p_copied)
#             name = target_bufftxt.value.decode('cp1251')
#             print(name)
#
#             lvitem.iItem = ctypes.c_int32(i)
#             p_buffer_lvi = VirtualAllocEx(h_process, 0, MAX_LEN, MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE)
#             WriteProcessMemory(h_process, p_buffer_lvi, ctypes.addressof(lvitem), ctypes.sizeof(LVITEMW), p_copied)
#
#             SendMessage(hwnd, LVM_GETITEMW, 0, p_buffer_lvi)
#             ReadProcessMemory(h_process, p_buffer_lvi, ctypes.addressof(lvitem), ctypes.sizeof(LVITEMW), p_copied)
#             print(lvitem.iImage)
#             # quit()
#
#             # Get icon position
#             p = POINT()
#             SendMessage(hwnd, LVM_GETITEMPOSITION, i, p_buffer_point)
#             ReadProcessMemory(h_process, p_buffer_point, ctypes.addressof(p), ctypes.sizeof(POINT), p_copied)
#
#             rect = RECT()
#             rect.left = LVIR_BOUNDS
#
#             SendMessage(hwnd, LVM_GETITEMRECT, i, p_buffer_rect)
#             ReadProcessMemory(h_process, p_buffer_rect, ctypes.addressof(rect), ctypes.sizeof(RECT), p_copied)
#
#             print(name)
#             # icons_list.append((i, name, p, rect))
#
#     finally:
#         try:
#             VirtualFreeEx(h_process, p_buffer_lvi, 0, MEM_RELEASE)
#         except:
#             pass
#
#         try:
#             VirtualFreeEx(h_process, buffer_txt, 0, MEM_RELEASE)
#         except:
#             pass
#
#         try:
#             VirtualFreeEx(h_process, p_buffer_point, 0, MEM_RELEASE)
#         except:
#             pass
#
#         try:
#             VirtualFreeEx(h_process, p_buffer_rect, 0, MEM_RELEASE)
#         except:
#             pass
#
#         try:
#             CloseHandle(h_process)
#         except:
#             pass
#
#     return icons_list


def get_desktop_image_icon(index):
    import struct
    import ctypes
    from commctrl import LVIF_IMAGE, LVM_GETITEMW
    from win32con import PROCESS_ALL_ACCESS, MEM_RESERVE, MEM_COMMIT, PAGE_READWRITE, MEM_RELEASE

    GetWindowThreadProcessId = ctypes.windll.user32.GetWindowThreadProcessId
    SendMessage = ctypes.windll.user32.SendMessageW
    OpenProcess = ctypes.windll.kernel32.OpenProcess
    VirtualAllocEx = ctypes.windll.kernel32.VirtualAllocEx
    WriteProcessMemory = ctypes.windll.kernel32.WriteProcessMemory
    ReadProcessMemory = ctypes.windll.kernel32.ReadProcessMemory
    VirtualFreeEx = ctypes.windll.kernel32.VirtualFreeEx
    CloseHandle = ctypes.windll.kernel32.CloseHandle

    MAX_LEN = 4096

    try:
        hwnd = GetDesktopListViewHandle()
        pid = ctypes.create_string_buffer(4)
        p_pid = ctypes.addressof(pid)
        GetWindowThreadProcessId(hwnd, p_pid)

        h_process = OpenProcess(PROCESS_ALL_ACCESS, False, struct.unpack("i", pid)[0])

        copied = ctypes.create_string_buffer(4)
        p_copied = ctypes.addressof(copied)

        lvitem = LVITEMW()
        lvitem.mask = ctypes.c_uint32(LVIF_IMAGE)
        lvitem.iItem = ctypes.c_int32(index)
        lvitem.iSubItem = ctypes.c_int32(0)

        p_buffer_lvi = VirtualAllocEx(h_process, 0, MAX_LEN, MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE)
        WriteProcessMemory(h_process, p_buffer_lvi, ctypes.addressof(lvitem), ctypes.sizeof(LVITEMW), p_copied)

        SendMessage(hwnd, LVM_GETITEMW, 0, p_buffer_lvi)
        ReadProcessMemory(h_process, p_buffer_lvi, ctypes.addressof(lvitem), ctypes.sizeof(LVITEMW), p_copied)
        return lvitem.iImage

    finally:
        try:
            VirtualFreeEx(h_process, p_buffer_lvi, 0, MEM_RELEASE)
        except:
            pass

        try:
            CloseHandle(h_process)
        except:
            pass


def ListView_GetImageList(hwnd, i_image_list):
    """

    Gets the handle to an image list used for drawing list-view items. You can use this macro or send the LVM_GETIMAGELIST message explicitly.

    Original:
    #define ListView_GetImageList(w,i) (HIMAGELIST)SNDMSG((w),LVM_GETIMAGELIST,(i),0)

    :param hwnd:
    :param i_image_list:
    :return:
    """

    import ctypes
    SendMessage = ctypes.windll.user32.SendMessageW

    from commctrl import LVM_GETIMAGELIST

    return SendMessage(hwnd, LVM_GETIMAGELIST, i_image_list, 0)


print(get_desktop_image_icon(0))  # 11
print(get_desktop_image_icon(1))  # 12
print(get_desktop_image_icon(2))  # 13

hwnd = GetDesktopListViewHandle()
print(hwnd)  # 65784

from commctrl import LVSIL_NORMAL, ILD_IMAGE
h_il = ListView_GetImageList(hwnd, LVSIL_NORMAL)
print(h_il)  # 860139888

from win32gui import ImageList_GetIcon
print(ImageList_GetIcon(h_il, 0, ILD_IMAGE))  # 0
print(ImageList_GetIcon(h_il, 11, ILD_IMAGE))  # 0


# typedef struct _IMAGEINFO {
#   HBITMAP hbmImage;
#   HBITMAP hbmMask;
#   int     Unused1;
#   int     Unused2;
#   RECT    rcImage;
# } IMAGEINFO, *LPIMAGEINFO;

import ctypes.wintypes
class IMAGEINFO(ctypes.Structure):
    _fields_ = [
        ('hbmImage', ctypes.wintypes.HBITMAP),
        ('hbmMask', ctypes.wintypes.HBITMAP),
        ('Unused1', ctypes.c_int),
        ('Unused2', ctypes.c_int),
        ('rcImage', ctypes.wintypes.RECT),
    ]

ImageList_GetImageInfo = ctypes.windll.comctl32.ImageList_GetImageInfo
# BOOL ImageList_GetImageInfo(
#    HIMAGELIST himl,
#    int        i,
#    IMAGEINFO  *pImageInfo
# );

pImageInfo = IMAGEINFO()
print(ImageList_GetImageInfo(h_il, 0, ctypes.byref(pImageInfo)))  # 0
print(ImageList_GetImageInfo(h_il, 11, ctypes.byref(pImageInfo)))  # 0




# import struct
#
# from PIL import Image
# from PIL.ImageOps import flip
#
# import ctypes
# from ctypes import wintypes
# windll = ctypes.windll
# user32 = windll.user32
# gdi32 = windll.gdi32
#
#
# class RECT(ctypes.Structure):
#     _fields_ = [
#         ('left', ctypes.c_long),
#         ('top', ctypes.c_long),
#         ('right', ctypes.c_long),
#         ('bottom', ctypes.c_long)
#     ]
#
#
# class BITMAPINFOHEADER(ctypes.Structure):
#     _fields_ = [
#         ("biSize", wintypes.DWORD),
#         ("biWidth", ctypes.c_long),
#         ("biHeight", ctypes.c_long),
#         ("biPlanes", wintypes.WORD),
#         ("biBitCount", wintypes.WORD),
#         ("biCompression", wintypes.DWORD),
#         ("biSizeImage", wintypes.DWORD),
#         ("biXPelsPerMeter", ctypes.c_long),
#         ("biYPelsPerMeter", ctypes.c_long),
#         ("biClrUsed", wintypes.DWORD),
#         ("biClrImportant", wintypes.DWORD)
#     ]
#
#
# class BITMAPINFO(ctypes.Structure):
#     _fields_ = [
#         ("bmiHeader", BITMAPINFOHEADER)
#     ]
#
#
# class BITMAP(ctypes.Structure):
#     _fields_ = [
#         ("bmType", ctypes.c_long),
#         ("bmWidth", ctypes.c_long),
#         ("bmHeight", ctypes.c_long),
#         ("bmWidthBytes", ctypes.c_long),
#         ("bmPlanes", wintypes.WORD),
#         ("bmBitsPixel", wintypes.WORD),
#         ("bmBits", ctypes.c_void_p)
#     ]
#
#
# def get_window_image(whandle):
#     def round_up32(n):
#         multiple = 32
#
#         while multiple < n:
#             multiple += 32
#
#         return multiple
#
#     rect = RECT()
#     user32.GetClientRect(whandle, ctypes.byref(rect))
#     bbox = (rect.left, rect.top, rect.right, rect.bottom)
#
#     hdcScreen = user32.GetDC(None)
#     hdc = gdi32.CreateCompatibleDC(hdcScreen)
#     hbmp = gdi32.CreateCompatibleBitmap(
#         hdcScreen,
#         bbox[2] - bbox[0],
#         bbox[3] - bbox[1]
#     )
#     gdi32.SelectObject(hdc, hbmp)
#
#     PW_CLIENTONLY = 1
#
#     if not user32.PrintWindow(whandle, hdc, PW_CLIENTONLY):
#         raise Exception("PrintWindow failed")
#
#     bmap = BITMAP()
#     if not gdi32.GetObjectW(hbmp, ctypes.sizeof(BITMAP), ctypes.byref(bmap)):
#         raise Exception("GetObject failed")
#
#     if bmap.bmBitsPixel != 32:
#         raise Exception("WTF")
#
#     scanline_len = round_up32(bmap.bmWidth * bmap.bmBitsPixel)
#     data_len = scanline_len * bmap.bmHeight
#
#     # http://msdn.microsoft.com/en-us/library/ms969901.aspx
#     bminfo = BITMAPINFO()
#     bminfo.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
#     bminfo.bmiHeader.biWidth = bmap.bmWidth
#     bminfo.bmiHeader.biHeight = bmap.bmHeight
#     bminfo.bmiHeader.biPlanes = 1
#     bminfo.bmiHeader.biBitCount = 24  # bmap.bmBitsPixel
#     bminfo.bmiHeader.biCompression = 0
#
#     data = ctypes.create_string_buffer(data_len)
#
#     DIB_RGB_COLORS = 0
#
#     get_bits_success = gdi32.GetDIBits(
#         hdc, hbmp,
#         0, bmap.bmHeight,
#         ctypes.byref(data), ctypes.byref(bminfo),
#         DIB_RGB_COLORS
#     )
#     if not get_bits_success:
#         raise Exception("GetDIBits failed")
#
#     # http://msdn.microsoft.com/en-us/library/dd183376%28v=vs.85%29.aspx
#     bmiheader_fmt = "LllHHLLllLL"
#
#     unpacked_header = [
#         bminfo.bmiHeader.biSize,
#         bminfo.bmiHeader.biWidth,
#         bminfo.bmiHeader.biHeight,
#         bminfo.bmiHeader.biPlanes,
#         bminfo.bmiHeader.biBitCount,
#         bminfo.bmiHeader.biCompression,
#         bminfo.bmiHeader.biSizeImage,
#         bminfo.bmiHeader.biXPelsPerMeter,
#         bminfo.bmiHeader.biYPelsPerMeter,
#         bminfo.bmiHeader.biClrUsed,
#         bminfo.bmiHeader.biClrImportant
#     ]
#
#     # Indexes: biXPelsPerMeter = 7, biYPelsPerMeter = 8
#     # Value from http://stackoverflow.com/a/23982267/2065904
#     unpacked_header[7] = 3779
#     unpacked_header[8] = 3779
#
#     image_header = struct.pack(bmiheader_fmt, *unpacked_header)
#
#     image = image_header + data
#
#     return flip(Image.frombytes("RGB", (bmap.bmWidth, bmap.bmHeight), image))
#
# import ctypes
#
# def GetDesktopListViewHandle():
#     """
#     Функция возвращает указатель на ListView рабочего стола.
#
#     Оригинал:
#     function GetDesktopListViewHandle: THandle;
#         var
#             S: string;
#         begin
#             Result := FindWindow('ProgMan', nil);
#             Result := GetWindow(Result, GW_CHILD);
#             Result := GetWindow(Result, GW_CHILD);
#             SetLength(S, 40);
#             GetClassName(Result, PChar(S), 39);
#             if PChar(S) <> 'SysListView32' then
#                 Result := 0;
#         end;
#
#     """
#
#     import ctypes
#     FindWindow = ctypes.windll.user32.FindWindowW
#     GetWindow = ctypes.windll.user32.GetWindow
#
#     def GetClassName(hwnd):
#         buff = ctypes.create_unicode_buffer(100)
#         ctypes.windll.user32.GetClassNameW(hwnd, buff, 99)
#         return buff.value
#
#     from win32con import GW_CHILD
#
#     # Ищем окно с классом "Progman" ("Program Manager")
#     hwnd = FindWindow('Progman', None)
#     hwnd = GetWindow(hwnd, GW_CHILD)  # SHELLDLL_DefView
#     hwnd = GetWindow(hwnd, GW_CHILD)  # SysListView32
#
#     if GetClassName(hwnd) != 'SysListView32':
#         return 0
#
#     return hwnd
#
# im = get_window_image(GetDesktopListViewHandle())
# print(im)
# im.show()
#
# quit()

# import ctypes
#
# def GetDesktopListViewHandle():
#     """
#     Функция возвращает указатель на ListView рабочего стола.
#
#     Оригинал:
#     function GetDesktopListViewHandle: THandle;
#         var
#             S: string;
#         begin
#             Result := FindWindow('ProgMan', nil);
#             Result := GetWindow(Result, GW_CHILD);
#             Result := GetWindow(Result, GW_CHILD);
#             SetLength(S, 40);
#             GetClassName(Result, PChar(S), 39);
#             if PChar(S) <> 'SysListView32' then
#                 Result := 0;
#         end;
#
#     """
#
#     import ctypes
#     FindWindow = ctypes.windll.user32.FindWindowW
#     GetWindow = ctypes.windll.user32.GetWindow
#
#     def GetClassName(hwnd):
#         buff = ctypes.create_unicode_buffer(100)
#         ctypes.windll.user32.GetClassNameW(hwnd, buff, 99)
#         return buff.value
#
#     from win32con import GW_CHILD
#
#     # Ищем окно с классом "Progman" ("Program Manager")
#     hwnd = FindWindow('Progman', None)
#     hwnd = GetWindow(hwnd, GW_CHILD)  # SHELLDLL_DefView
#     hwnd = GetWindow(hwnd, GW_CHILD)  # SysListView32
#
#     if GetClassName(hwnd) != 'SysListView32':
#         return 0
#
#     return hwnd
#
#
# class LVITEMW(ctypes.Structure):
#     _fields_ = [
#         ('mask', ctypes.c_uint32),
#         ('iItem', ctypes.c_int32),
#         ('iSubItem', ctypes.c_int32),
#         ('state', ctypes.c_uint32),
#         ('stateMask', ctypes.c_uint32),
#         ('pszText', ctypes.c_uint64),
#         ('cchTextMax', ctypes.c_int32),
#         ('iImage', ctypes.c_int32),
#         ('lParam', ctypes.c_uint64),  # On 32 bit should be c_long
#         ('iIndent', ctypes.c_int32),
#         ('iGroupId', ctypes.c_int32),
#         ('cColumns', ctypes.c_uint32),
#         ('puColumns', ctypes.c_uint64),
#         ('piColFmt', ctypes.c_int64),
#         ('iGroup', ctypes.c_int32),
#     ]
#
#
# def get_desktop_process_handle(hwnd=None):
#     import ctypes
#     import struct
#     from win32con import PROCESS_ALL_ACCESS
#
#     GetWindowThreadProcessId = ctypes.windll.user32.GetWindowThreadProcessId
#     OpenProcess = ctypes.windll.kernel32.OpenProcess
#
#     if hwnd is None:
#         hwnd = GetDesktopListViewHandle()
#
#     pid = ctypes.create_string_buffer(4)
#     p_pid = ctypes.addressof(pid)
#     GetWindowThreadProcessId(hwnd, p_pid)
#
#     return OpenProcess(PROCESS_ALL_ACCESS, False, struct.unpack("i", pid)[0])
#
#
# def get_desktop_image_icon(index):
#     import ctypes
#     from commctrl import LVIF_IMAGE, LVM_GETITEMW
#     from win32con import MEM_RESERVE, MEM_COMMIT, PAGE_READWRITE, MEM_RELEASE
#
#     SendMessage = ctypes.windll.user32.SendMessageW
#     VirtualAllocEx = ctypes.windll.kernel32.VirtualAllocEx
#     WriteProcessMemory = ctypes.windll.kernel32.WriteProcessMemory
#     ReadProcessMemory = ctypes.windll.kernel32.ReadProcessMemory
#     VirtualFreeEx = ctypes.windll.kernel32.VirtualFreeEx
#     CloseHandle = ctypes.windll.kernel32.CloseHandle
#
#     MAX_LEN = 4096
#
#     try:
#         hwnd = GetDesktopListViewHandle()
#         h_process = get_desktop_process_handle(hwnd)
#
#         copied = ctypes.create_string_buffer(4)
#         p_copied = ctypes.addressof(copied)
#
#         lvitem = LVITEMW()
#         lvitem.mask = ctypes.c_uint32(LVIF_IMAGE)
#         lvitem.iItem = ctypes.c_int32(index)
#         lvitem.iSubItem = ctypes.c_int32(0)
#
#         p_buffer_lvi = VirtualAllocEx(h_process, 0, MAX_LEN, MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE)
#         WriteProcessMemory(h_process, p_buffer_lvi, ctypes.addressof(lvitem), ctypes.sizeof(LVITEMW), p_copied)
#
#         SendMessage(hwnd, LVM_GETITEMW, 0, p_buffer_lvi)
#         ReadProcessMemory(h_process, p_buffer_lvi, ctypes.addressof(lvitem), ctypes.sizeof(LVITEMW), p_copied)
#         return lvitem.iImage
#
#     finally:
#         try:
#             VirtualFreeEx(h_process, p_buffer_lvi, 0, MEM_RELEASE)
#         except:
#             pass
#
#         try:
#             CloseHandle(h_process)
#         except:
#             pass
#
#
# # h_process = get_desktop_process_handle()
# # print(h_process)
#
# # LoadImage = ctypes.windll.user32.LoadImageW
#
# # ctypes.wintypes.windll.user32.LoadImageW(defs.NULL, unicode(icon, 'mbcs'), defs.IMAGE_ICON, 0, 0, defs.LR_LOADFROMFILE);
# # LoadImage = ctypes.wintypes.windll.user32.LoadImageW
# #
# # LoadImage
# # _In_opt_ HINSTANCE hinst,
# # _In_     LPCTSTR   lpszName,
# # _In_     UINT      uType,
# # _In_     int       cxDesired,
# # _In_     int       cyDesired,
# # _In_     UINT      fuLoad
#
# # hBitmap =(HBITMAP)LoadImage(NULL,"C:\\test.bmp",IMAGE_BITMAP,0,0,LR_LOADFROMFILE);
#
#
# # def MAKEINTRESOURCE(i):
# #     """
# #
# #     #define MAKEINTRESOURCEW(i) ((LPWSTR)((ULONG_PTR)((WORD)(i))))
# #     """
# #
# #     return str(hex(i))
# #
# # from win32gui import IMAGE_BITMAP, LR_DEFAULTSIZE, ImageList_GetIcon
# # print(MAKEINTRESOURCE(id_image))
# # # h_bitmap = LoadImage(h_process, MAKEINTRESOURCE(id_image), IMAGE_IC, LR_DEFAULTSIZE, LR_DEFAULTSIZE, LR_DEFAULTSIZE)
# # # print(h_bitmap)
#
#
# def ListView_GetImageList(hwnd, i_image_list):
#     """
#
#     This retrieves the handle to an image list used for drawing list-view items.
#     You can use this or send the LVM_GETIMAGELIST message explicitly.
#
#     Original:
#     #define ListView_GetImageList(w,i) (HIMAGELIST)SNDMSG((w),LVM_GETIMAGELIST,(i),0)
#
#     :param hwnd: Handle to the list-view control.
#     :param i_image_list: Image list to retrieve. It is one of the following values.
#         Value	Description
#         LVSIL_NORMAL Image list with large icons. (LVSIL_NORMAL = 0)
#         LVSIL_SMALL	Image list with small icons. (LVSIL_SMALL = 1)
#         LVSIL_STATE	Image list with state images. (LVSIL_STATE = 2)
#     :return:
#     """
#
#     import ctypes
#     SendMessage = ctypes.windll.user32.SendMessageW
#
#     from commctrl import LVM_GETIMAGELIST
#
#     return SendMessage(hwnd, LVM_GETIMAGELIST, i_image_list, 0)
#
#
# from commctrl import LVSIL_NORMAL
# hwnd = GetDesktopListViewHandle()
# print(hwnd)
#
# # h_process = get_desktop_process_handle(hwnd)
# # print(h_process)
#
# himl = ListView_GetImageList(hwnd, LVSIL_NORMAL)
# print(himl)
#
# id_image = get_desktop_image_icon(0)
# print(id_image)
#
# from win32gui import ImageList_GetIcon, ILD_NORMAL, ILD_TRANSPARENT, DestroyIcon
# h_icon = ImageList_GetIcon(himl, id_image, ILD_NORMAL | ILD_TRANSPARENT)
# h_icon = ImageList_GetIcon(himl, id_image, ILD_NORMAL)
# print(h_icon)


# winapi_qt_get_icon_file_name.py



# ImageList_GetIconSize = ctypes.windll.comctl32.ImageList_GetIconSize
# # ImageList_ExtractIcon = ctypes.windll.comctl32.ImageList_ExtractIcon
# cx = ctypes.c_int()
# cy = ctypes.c_int()
# print(ImageList_GetIconSize(himl, ctypes.byref(cx), ctypes.byref(cy)), cx, cy)
# # from win32gui import ImageList_GetIconSize

# px = QPixmap.fromWinHICON(hIcon)
# DestroyIcon(hIcon)

# print(LoadImage(defs.NULL, unicode(icon, 'mbcs'), defs.IMAGE_ICON, 0, 0, defs.LR_LOADFROMFILE))



def get_desktop_image_icon(index):
    import struct
    import ctypes
    from commctrl import LVIF_IMAGE, LVM_GETITEMW
    from win32con import PROCESS_ALL_ACCESS, MEM_RESERVE, MEM_COMMIT, PAGE_READWRITE, MEM_RELEASE

    GetWindowThreadProcessId = ctypes.windll.user32.GetWindowThreadProcessId
    SendMessage = ctypes.windll.user32.SendMessageW
    OpenProcess = ctypes.windll.kernel32.OpenProcess
    VirtualAllocEx = ctypes.windll.kernel32.VirtualAllocEx
    WriteProcessMemory = ctypes.windll.kernel32.WriteProcessMemory
    ReadProcessMemory = ctypes.windll.kernel32.ReadProcessMemory
    VirtualFreeEx = ctypes.windll.kernel32.VirtualFreeEx
    CloseHandle = ctypes.windll.kernel32.CloseHandle

    MAX_LEN = 4096

    try:
        hwnd = GetDesktopListViewHandle()
        pid = ctypes.create_string_buffer(4)
        p_pid = ctypes.addressof(pid)
        GetWindowThreadProcessId(hwnd, p_pid)

        h_process = OpenProcess(PROCESS_ALL_ACCESS, False, struct.unpack("i", pid)[0])

        copied = ctypes.create_string_buffer(4)
        p_copied = ctypes.addressof(copied)

        lvitem = LVITEMW()
        lvitem.mask = ctypes.c_uint32(LVIF_IMAGE)
        lvitem.iItem = ctypes.c_int32(index)
        lvitem.iSubItem = ctypes.c_int32(0)

        p_buffer_lvi = VirtualAllocEx(h_process, 0, MAX_LEN, MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE)
        WriteProcessMemory(h_process, p_buffer_lvi, ctypes.addressof(lvitem), ctypes.sizeof(LVITEMW), p_copied)

        SendMessage(hwnd, LVM_GETITEMW, 0, p_buffer_lvi)
        ReadProcessMemory(h_process, p_buffer_lvi, ctypes.addressof(lvitem), ctypes.sizeof(LVITEMW), p_copied)
        return lvitem.iImage

    finally:
        try:
            VirtualFreeEx(h_process, p_buffer_lvi, 0, MEM_RELEASE)
        except:
            pass

        try:
            CloseHandle(h_process)
        except:
            pass


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
