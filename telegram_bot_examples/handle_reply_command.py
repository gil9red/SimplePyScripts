#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install python-telegram-bot
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import MessageHandler, CommandHandler, Filters, CallbackContext

from common import get_logger, log_func, start_bot, run_main


COMMANDS = ["say", "echo", "123"]
REPLY_KEYBOARD_MARKUP = ReplyKeyboardMarkup.from_row(COMMANDS, resize_keyboard=True)

log = get_logger(__file__)


@log_func(log)
def on_start(update: Update, _: CallbackContext):
    update.effective_message.reply_text("Write something")


@log_func(log)
def on_request(update: Update, _: CallbackContext):
    message = update.effective_message

    message.reply_text("Echo: " + message.text, reply_markup=REPLY_KEYBOARD_MARKUP)


@log_func(log)
def on_reply_command(update: Update, _: CallbackContext):
    message = update.effective_message

    message.reply_text(
        "Reply command: " + message.text, reply_markup=REPLY_KEYBOARD_MARKUP
    )


def main():
    handlers = [
        CommandHandler("start", on_start),
        MessageHandler(Filters.text(COMMANDS), on_reply_command),
        MessageHandler(Filters.text, on_request),
    ]
    start_bot(log, handlers)


if __name__ == "__main__":
    run_main(main, log)
