#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT

# pip install python-telegram-bot
from telegram import Update
from telegram.ext import MessageHandler, CommandHandler, Filters, CallbackContext

from common import get_logger, log_func, start_bot, run_main


log = get_logger(__file__)


CHAT_BY_DATETIME = dict()


@log_func(log)
def on_start(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        'Write something'
    )


@log_func(log)
def on_request(update: Update, context: CallbackContext):
    message = update.effective_message

    text = 'Получено!'
    seconds = 5
    current_time = DT.datetime.now()
    last_datetime = CHAT_BY_DATETIME.get(message.chat_id)

    # Если первое сообщение (время не задано)
    if not last_datetime:
        CHAT_BY_DATETIME[message.chat_id] = current_time
    else:
        # Если с последнего сообщения прошло не больше секунд, чем задано
        if (current_time - last_datetime).total_seconds() <= seconds:
            text = f'Подождите {seconds} секунд перед выполнение этой команды'
        else:
            CHAT_BY_DATETIME[message.chat_id] = current_time

    message.reply_text(text, quote=True)


def main():
    handlers = [
        CommandHandler('start', on_start),
        MessageHandler(Filters.text, on_request),
    ]
    start_bot(log, handlers)


if __name__ == '__main__':
    run_main(main, log)
