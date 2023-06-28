#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://core.telegram.org/bots/api#sendphoto
#         https://core.telegram.org/bots/api#photosize
#         https://core.telegram.org/bots/api#sending-files


# pip install python-telegram-bot
from telegram import Update
from telegram.ext import MessageHandler, CommandHandler, Filters, CallbackContext

from common import get_logger, log_func, start_bot, run_main


log = get_logger(__file__)


@log_func(log)
def on_start(update: Update, _: CallbackContext):
    update.effective_message.reply_text(
        "Отправка картинки боту вернет её с file_id\n"
        "Отправка текстом file_id вернет картинку"
    )


@log_func(log)
def on_request(update: Update, _: CallbackContext):
    message = update.effective_message
    file_id = message.text

    try:
        message.reply_photo(file_id, quote=True)
    except Exception as e:
        message.reply_text(f"Error: {e}")
        raise e


@log_func(log)
def on_photo(update: Update, _: CallbackContext):
    message = update.effective_message

    photo_large = max(message.photo, key=lambda x: (x.width, x.height))
    file_id = photo_large.file_id

    message.reply_photo(file_id, caption=f"file_id: {file_id}", quote=True)


def main():
    handlers = [
        CommandHandler("start", on_start),
        MessageHandler(Filters.text, on_request),
        MessageHandler(Filters.photo, on_photo),
    ]
    start_bot(log, handlers)


if __name__ == "__main__":
    run_main(main, log)
