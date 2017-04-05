#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# https://good-developers.com/prostoj-telegram-bot/#comment-5427


# Импортировать модули телеграма
from telegram import Updater, Emoji, ParseMode
import telegram
from time import sleep
#
import logging
import requests, json
import urllib.request, urllib.parse, urllib
import urllib.request
import re, sys, os, platform
import random  as  random_number

#
# Переменные и Запросы
help_text = 'Текст, который будет выводиться при команде /help'
#
# Юзер новый заходит в чат
welcome_text = 'Текст, который будет выводиться, когда юзер заходит в чат'
#
# Юзер покидает чат
goodbuy_text = 'Текст, который будет выводиться, когда юзер выходит из чата'
#
# Локальный IP адрес
MY_IP = '1.2.3.4'
# Будет такой себе переключатель. Когда True - обрабатывать сообщения
# Когда False - не принимать сообщения
WORK = True
# ID чата админа и его Username
ADMIN_CHAT = '1234567'
ADMIN_USERNAME = "@username"
# Адрес хранения мультимедиа
IMG_URI = 'https://vsbot.good-developers.com/'
#
# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


#
#

# Отправка сообщения на команду /help
def help(bot, update):
    bot.sendMessage(update.message.chat_id, text=help_text, parse_mode=ParseMode.MARKDOWN)
# Отправка ошибки в чат админу
def error(bot, update, error):
    bot.sendMessage(ADMIN_CHAT, text=error, parse_mode=ParseMode.MARKDOWN)
# Отправка сообщения на команду /start
def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Привет! Набери /help и получишь список команд.")
#
#
# Поиск на YouTube
def video(bot, update,msg):
    link = urllib.parse.urlencode({"search_query" : msg})
    content = urllib.request.urlopen("https://www.youtube.com/results?" + link)
    search_results = re.findall('href=\"\/watch\?v=(.*?)\"', content.read().decode())
    if len(search_results)>0:
        # Первые 10 результатов
        search_results = search_results[0:9:1]
        choice_f = random_number.choice(search_results)
        yt_link = "https://www.youtube.com/watch?v="+choice_f
        bot.sendMessage(update.message.chat_id, text=yt_link, parse_mode=ParseMode.MARKDOWN)
    else:
        bot.sendMessage(update.message.chat_id, text='Ничего не найдено.')
#
# Поиск Картинки на Яндексе
def pic(bot, update, msg):
    ss = requests.Session()
    r = ss.get('https://yandex.ua/images/search?text='+msg)
    p = 'div.class\=\"serp-item.*?url\"\:\"(.*?)\"'
    response = r.text
    w = re.findall(p,response)
    #
    if len(w)>0:
        # Первые 30 фото
        w = w[0:29:1]
        choice_f = random_number.choice(w)
        bot.sendPhoto(update.message.chat_id, photo=choice_f)
    else:
        bot.sendMessage(update.message.chat_id, 'Ничего не найдено')
#
# Получить первую ссылку
def g(bot, update, msg):
    f = { 'v' : '1.0', 'q' : msg, 'userip' : MY_IP}
    g_search = urllib.parse.urlencode(f)
    s = requests.Session()
    url = ('https://ajax.googleapis.com/ajax/services/search/web?'+g_search)
    r = s.get(url,cookies={'my': 'browser'})
    response = r.text
    #
    pattern = '\"GwebSearch\","unescapedUrl\"\:\"(.*?)\"'
    g_search = re.findall(pattern,response)
    if len(g_search)>0:
        g_search = g_search[0]
        g_search = g_search.replace('\\u0026','&amp;')
        g_search = g_search.replace('\\u003d','=')
        bot.sendMessage(update.message.chat_id, text=g_search, parse_mode=ParseMode.MARKDOWN)
    else:
        bot.sendMessage(update.message.chat_id, text='Ничего не найдено.')
#
#
# Обработка команд!
def do_it(bot, update):
    msg = update.message.text
    global WORK
    if len(msg)>130:
        txt = 'Превышено ограничение в *130* символов для команды. ' \
              'Тут не *130*, а *'+str(len(msg))+'*!'
        bot.sendMessage(update.message.chat_id, text=txt, parse_mode=ParseMode.MARKDOWN)
        msg = ''
    # Поиск в Google
    cmd = ''
    pattern = '^!g (.*?)$'
    cmd = re.findall(pattern,msg)
    if len(cmd)>0:
        g(bot,update,cmd[0])
    # Поиск Картинки в Яндекс
    cmd = ''
    pattern = '^!pic (.*?)$'
    cmd = re.findall(pattern,msg)
    if len(cmd)>0:
        pic(bot,update,cmd[0])
    # Поиск видео на Yooutube
    cmd = ''
    pattern = '^!yt (.*?)$'
    cmd = re.findall(pattern,msg)
    if len(cmd)>0:
        video(bot,update,cmd[0])
    # Выключить бот
    cmd = ''
    pattern = '^!тихо$'
    cmd = re.findall(pattern,msg)
    if len(cmd)>0:
        WORK = False
        txt = 'Я ухожу. Напишите *'+ADMIN_USERNAME+'* что бы я вернулся.'
        bot.sendMessage(update.message.chat_id, text=txt, parse_mode=ParseMode.MARKDOWN)
#
# Анализ текста
def analyse_text(bot, update, words):
    msg = update.message.text
    # Перевод в нижний регистр
    msg = msg.lower()
    # Небольшой словарь
    a3 = ["привет бот","привет всем", "всем привет"]
    q3 = "Привет человек"
    #
    C_DIC = {q1:a1}
    # Считаем стандартные фразы
    for a, b in C_DIC.items():
        for c in b:
            if c in msg:
                # Типа бот печатает и сейчас ответит
                bot.sendChatAction(update.message.chat_id, action=telegram.ChatAction.TYPING)
                sleep(2)
                #ans = random_number.choice(a)
                bot.sendMessage(update.message.chat_id, text=a, parse_mode=ParseMode.MARKDOWN)
#
# Предварительный анализ сообщения
def think(bot, update):
    msg = update.message.text
    # Перевод в нижний регистр
    msg = msg.lower()
    # Количество слов узнаем
    p = '([a-zA-Zа-яА-Я]+)'
    words = re.findall(p,msg)
    msg_count = len(words)
    # Много наговорил
    if msg_count> 100:
        txt = 'Много написал, не понимаю!'
        bot.sendMessage(update.message.chat_id, text=txt, parse_mode=ParseMode.MARKDOWN)
    # Слишком много наговорил
    if msg_count>400:
        lnk = IMG_URI+'53L3fx6EJ7Fl9UiEzDRC.png'
        bot.sendPhoto(update.message.chat_id, photo=lnk)
    # Короткий текст
    if msg_count<100:
        analyse_text(bot, update, words)
#
# Обработка сообщения
def echo(bot, update):
    cid = update.message.chat_id
    # Проверка блокировки
    #print(update.message.text)
    global WORK
    global ADMIN_CHAT
    if WORK==False:
        if str(cid) != ADMIN_CHAT:
            update.message.text = ''
        else:
            # Ищем команду запуска
            cmd = ''
            pattern = '^!работай$'
            cmd = re.findall(pattern,update.message.text)
            if len(cmd)>0:
                WORK = True
                txt_r = 'Вернусь к работе!'
                bot.sendMessage(update.message.chat_id,
                                text=txt_r,
                                parse_mode=ParseMode.MARKDOWN)
    #
    msg = update.message.text
    # Новый или вышел
    if (update.message.new_chat_participant)!=None:
        bot.sendMessage(update.message.chat_id, text=welcome_text, parse_mode=ParseMode.MARKDOWN)
    if (update.message.left_chat_participant)!=None:
        bot.sendMessage(update.message.chat_id, text=goodbuy_text, parse_mode=ParseMode.MARKDOWN)
    # Проверяем поступила ли прямая команда
    cmd = ''
    pattern = '^!(.*?)$'
    cmd = re.findall(pattern,msg)
    if len(cmd)>0:
        do_it(bot, update)
    else:
        think(bot, update)
#


#
def main():
    # Создаем класс Updater и указываем текущий токен вашего бота
    updater = Updater("ТОКЕН")
    dp = updater.dispatcher
    # Задаем стандартные команды /help /start. Они должны быть установлены по умолчанию.
    dp.addTelegramCommandHandler("start", start)
    dp.addTelegramCommandHandler("help", help)
    dp.addTelegramMessageHandler(echo)
    # Добавляем обработку ошибок. Они будут записываться в функции error
    dp.addErrorHandler(error)
    # Запускаем
    updater.start_polling()
    updater.idle()
#
if __name__ == '__main__':
    main()
