#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as dt

# pip install python-telegram-bot
from telegram import Update
from telegram.ext import MessageHandler, CommandHandler, Filters, CallbackContext

from common import get_logger, log_func, start_bot, run_main


log = get_logger(__file__)


CHAT_BY_DATETIME = dict()


@log_func(log)
def on_start(update: Update, _: CallbackContext) -> None:
    update.effective_message.reply_text("Write something")


@log_func(log)
def on_request(update: Update, _: CallbackContext) -> None:
    message = update.effective_message

    text = "Получено!"
    need_seconds = 50
    current_time = dt.datetime.now()
    last_datetime = CHAT_BY_DATETIME.get(message.chat_id)

    # Если первое сообщение (время не задано)
    if not last_datetime:
        CHAT_BY_DATETIME[message.chat_id] = current_time
    else:
        # Разница в секундах между текущим временем и временем последнего сообщения
        delta_seconds = (current_time - last_datetime).total_seconds()

        # Осталось ждать секунд перед отправкой
        seconds_left = int(need_seconds - delta_seconds)

        # Если время ожидания не закончилось
        if seconds_left > 0:
            text = f"Подождите {seconds_left} секунд перед выполнение этой команды"
        else:
            CHAT_BY_DATETIME[message.chat_id] = current_time

    message.reply_text(text, quote=True)


def main() -> None:
    handlers = [
        CommandHandler("start", on_start),
        MessageHandler(Filters.text, on_request),
    ]
    start_bot(log, handlers)


if __name__ == "__main__":
    run_main(main, log)
