#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as dt

# pip install pyTelegramBotAPI
import telebot

from config import TOKEN


bot = telebot.TeleBot(TOKEN)


CHAT_BY_DATETIME = dict()


@bot.message_handler(commands=["help", "start"])
def on_start(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Write something")


@bot.message_handler(func=lambda message: True)
def on_request(message: telebot.types.Message):
    text = "Получено!"
    need_seconds = 50
    current_time = dt.datetime.now()
    last_datetime = CHAT_BY_DATETIME.get(message.chat.id)

    # Если первое сообщение (время не задано)
    if not last_datetime:
        CHAT_BY_DATETIME[message.chat.id] = current_time
    else:
        # Разница в секундах между текущим временем и временем последнего сообщения
        delta_seconds = (current_time - last_datetime).total_seconds()

        # Осталось ждать секунд перед отправкой
        seconds_left = int(need_seconds - delta_seconds)

        # Если время ожидания не закончилось
        if seconds_left > 0:
            text = f"Подождите {seconds_left} секунд перед выполнение этой команды"
        else:
            CHAT_BY_DATETIME[message.chat.id] = current_time

    bot.reply_to(message, text)


bot.infinity_polling()
