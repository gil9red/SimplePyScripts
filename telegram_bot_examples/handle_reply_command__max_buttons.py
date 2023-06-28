#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install python-telegram-bot
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import MessageHandler, CommandHandler, Filters, CallbackContext

from common import get_logger, log_func, start_bot, run_main


ROWS = 24
COLS = 12
rows = [[f"{i + 1}"] + ["x" for j in range(COLS - 1)] for i in range(ROWS)]

REPLY_KEYBOARD_MARKUP = ReplyKeyboardMarkup(rows, resize_keyboard=True)

log = get_logger(__file__)


@log_func(log)
def on_start(update: Update, _: CallbackContext):
    update.effective_message.reply_text("Write something")


@log_func(log)
def on_request(update: Update, _: CallbackContext):
    message = update.effective_message

    message.reply_text("Echo: " + message.text, reply_markup=REPLY_KEYBOARD_MARKUP)


def main():
    handlers = [
        CommandHandler("start", on_start),
        MessageHandler(Filters.text, on_request),
    ]
    start_bot(log, handlers)


if __name__ == "__main__":
    run_main(main, log)
