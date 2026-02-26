#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install pyTelegramBotAPI
import telebot

from config import TOKEN


bot = telebot.TeleBot(TOKEN)


data_year = {
    "01.01": "Новый год",
    "23.02": "23 февраля",
}


# SOURCE: https://ru.stackoverflow.com/questions/1264757
def func(message) -> None:
    text = message.text
    result = data_year.get(text, "В этот день праздников нет. Иди работать!")
    bot.send_message(message.from_user.id, result)


@bot.message_handler(content_types=["text"])
def get_text_messages(message) -> None:
    data = bot.send_message(
        message.from_user.id, "Введите дату в формате Д.ММ и нажмите ENTER"
    )
    bot.register_next_step_handler(data, func)


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

bot.polling(none_stop=True)
