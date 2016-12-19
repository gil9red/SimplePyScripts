#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


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


"""Advanced time-outs -- прогрессивные тайм-ауты
В случае неудачной попытки время следующей попытки откладывается на некоторую увеличивающуюся величину.

"""


def work():
    import random
    if random.randint(0, 5):
        raise Exception()

    print('Work!')


timeout = 0.5

# Для обеспечения повторных попыток выполнения используется цикл
while True:
    try:
        work()

        # Если не было исключений, прерываем цикл
        break

    except:
        print('Неудача с таймаутом {}.'.format(timeout))

        import time
        time.sleep(timeout)
        timeout += 0.1


quit()


"""Пример реализации алгоритма выделения предыдущей вкладки.

"""


from PyQt5.QtWidgets import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.prev_tab_index = -1
        self.curr_tab_index = 0

        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(QLabel('1'), '1')
        self.tab_widget.addTab(QLabel('2'), '2')
        self.tab_widget.addTab(QLabel('3'), '3')
        self.tab_widget.addTab(QLabel('4'), '4')
        self.tab_widget.addTab(QLabel('5'), '5')
        self.tab_widget.setCurrentIndex(self.curr_tab_index)

        self.tab_widget.currentChanged.connect(self.current_tab_changed)

        self.setCentralWidget(self.tab_widget)

    def current_tab_changed(self, i):
        # Запоминание индексов предыдущей и текущей вкладки.
        # При переключении вкладок:
        #   У предыдущей убирается выделение
        #   Текущий индекс становится предыдущей
        #   У новой предыдущей добавляется выделение

        if self.prev_tab_index != -1:
            prev_text = self.tab_widget.tabText(self.prev_tab_index)
            self.tab_widget.setTabText(self.prev_tab_index, prev_text[1:-1])

        self.prev_tab_index = self.curr_tab_index
        prev_text = self.tab_widget.tabText(self.prev_tab_index)
        self.tab_widget.setTabText(self.prev_tab_index, '_' + prev_text + '_')

        self.curr_tab_index = i


app = QApplication([])

mw = MainWindow()
mw.show()

app.exec()


quit()

def foo():
    while True:
        import time
        yield time.time()
        time.sleep(1)

for i in foo():
    print(i)

quit()

# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
#
# """
# Заполнение списка из функции без фриза окна. Вариант с QApplication.processEvents.
# """
#
#
# def foo():
#     for i in range(1000000):
#         yield i
#         QApplication.processEvents()
#
# app = QApplication([])
#
# lw = QListWidget()
# lw.show()
#
# for i in foo():
#     lw.addItem(str(i))
#     lw.scrollToBottom()
#
# app.exec_()


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

"""
Заполнение списка из функции без фриза окна. Вариант с QThread.
"""


import traceback
def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    text += ''.join(traceback.format_tb(tb))

    print('Error: ', text)

import sys
sys.excepthook = log_uncaught_exceptions


class MyThread(QThread):
    about_new_value = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.executed = False

    def run(self):
        print('start thread')

        try:
            for i in range(1000):
                if not self.executed:
                    break

                self.about_new_value.emit(i)
                print(i)

                # Задержка в 5 миллисекунд
                import time
                time.sleep(0.005)

        finally:
            print('finish thread')

    def start(self, priority=QThread.InheritPriority):
        self.executed = True

        return super().start(priority)

    def exit(self, returnCode=0):
        self.executed = False

        return super().exit(returnCode)


app = QApplication([])

lw = QListWidget()

def add(i):
    lw.addItem(str(i))
    lw.scrollToBottom()

    # Можно использовать, если форма фризится. Или просто у потока увеличить время задержки
    # QApplication.processEvents()


my_thread = MyThread()
my_thread.about_new_value.connect(add)

start_button = QPushButton('Start thread')
start_button.clicked.connect(my_thread.start)

stop_button = QPushButton('Stop thread')
stop_button.clicked.connect(my_thread.exit)

clear_button = QPushButton('Clear')
clear_button.clicked.connect(lw.clear)

layout = QVBoxLayout()
layout.addWidget(start_button)
layout.addWidget(stop_button)
layout.addWidget(clear_button)
layout.addWidget(lw)

w = QWidget()
w.setLayout(layout)
w.show()

app.exec_()


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



# import sys
# import random
#
# from PyQt5 import QtGui
# from PyQt5.QtGui import *
# from PyQt5.QtCore import *
#
#
# class MainWindow(QMainWindow, QWidget, QApplication):
#
#     def __init__(self, parent = None):
#         super(MainWindow, self).__init__(parent)
#
#         QTimer.singleShot(0, self.task)
#         # self.task()
#
#     def task(self):
#         self.taskbarButton = QWinTaskbarButton(self)
#         self.taskbarButton.setWindow(self.windowHandle())
#
#         self.taskbarProgress = self.taskbarButton.progress()
#
#         self.taskbarProgress.setRange(0, 100)
#         self.taskbarProgress.setVisible(True)
#         self.taskbarProgress.setValue(random.randint(0, 100))
#
#         self.taskbarProgress.show()
#
#
# if __name__ == '__main__':
#
#     app = QApplication(sys.argv)
#     mainWindow = MainWindow()
#     mainWindow.show()
#     sys.exit(app.exec_())
#
#
# quit()


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


# card_stren_p_1_list = [8, 11, 4, 8, 6, 12, 10, 1, 5, 11, 7, 0, 9, 11, 1, 0, 10, 12, 9, 5, 11, 8, 2, 12, 3, 3]
# card_stren_p_2_list = [0, 7, 6, 2, 3, 12, 9, 10, 5, 3, 2, 4, 4, 10, 7, 8, 2, 9, 4, 1, 6, 1, 5, 7, 6, 0]
#
# # # Список карт преобразуется в список сил карт
# # card_stren_p_1_list = [strongest_card.index(i[:len(i) - 1]) for i in cardp_1_list]
# # card_stren_p_2_list = [strongest_card.index(i[:len(i) - 1]) for i in cardp_2_list]
# # print(card_stren_p_1_list, file=sys.stderr)
# # print(card_stren_p_2_list, file=sys.stderr)
#
# # Стек карт, полученных в "войне" первого и второго игрока
# war_stack_1 = list()
# war_stack_2 = list()
#
# winner = None
# turn = 0
#
# # Ограничение количества итераций бесконечного цикла
# count = 1000
#
#
# class FindWinnerException(Exception):
#     def __init__(self, winner):
#         self.winner = winner
#
#
# def fight():
#     if not card_stren_p_1_list:
#         raise FindWinnerException(2)
#
#     if not card_stren_p_2_list:
#         raise FindWinnerException(1)
#
#     card_p_1 = card_stren_p_1_list.pop(0)
#     card_p_2 = card_stren_p_2_list.pop(0)
#
#     if card_p_1 > card_p_2:
#         while war_stack_1:
#             card_stren_p_1_list.append(war_stack_1.pop(0))
#
#         while war_stack_2:
#             card_stren_p_1_list.append(war_stack_2.pop(0))
#
#         card_stren_p_1_list.append(card_p_1)
#         card_stren_p_1_list.append(card_p_2)
#
#     elif card_p_1 < card_p_2:
#         while war_stack_1:
#             card_stren_p_2_list.append(war_stack_1.pop(0))
#
#         while war_stack_2:
#             card_stren_p_2_list.append(war_stack_2.pop(0))
#
#         card_stren_p_2_list.append(card_p_1)
#         card_stren_p_2_list.append(card_p_2)
#     else:
#         war()
#
#     if not card_stren_p_1_list:
#         raise FindWinnerException(2)
#
#     if not card_stren_p_2_list:
#         raise FindWinnerException(1)
#
#
# def war():
#     for _ in range(3):
#         if not card_stren_p_1_list:
#             raise FindWinnerException(2)
#
#         if not card_stren_p_2_list:
#             raise FindWinnerException(1)
#
#         war_stack_1.append(card_stren_p_1_list.pop(0))
#         war_stack_2.append(card_stren_p_2_list.pop(0))
#
#     fight()
#
#
# while True:
#     try:
#         turn += 1
#
#         count -= 1
#         if count <= 0:
#             break
#
#         fight()
#
#         # print(turn, file=sys.stderr)
#         # print(card_stren_p_1_list, file=sys.stderr)
#         # print(card_stren_p_2_list, file=sys.stderr)
#         # print('', file=sys.stderr)
#
#     except FindWinnerException as e:
#         winner = e.winner
#         break
#
# if winner is None:
#     raise Exception('Unknown winner')
#
# print("{} {}".format(winner, turn))
# # print("PAT")
#
#
# quit()
#

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


# http://habrahabr.ru/post/192102/
# http://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html
#
# def gen_sudoku(n=3):
#     return [[((i*n + i//n + j) % (n*n) + 1) for j in range(n*n)] for i in range(n*n)]
#
# for row in gen_sudoku():
#     print(row)
#


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


# TODO: service parse.com
# https://parse.com
# https://parse.com/docs/api_libraries
# https://github.com/dgrtwo/ParsePy
# http://habrahabr.ru/post/246989/


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


# TODO: больше примеров работы с модулями py
# http://pythonworld.ru/karta-sajta


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

# TODO: https://docs.python.org/3/tutorial/stdlib2.html
# import textwrap
# text = 'Придумать простое приложение и реализовать его с помощью TDD (используя unit-тесты)'
# print(textwrap.fill(text, width=45))


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
