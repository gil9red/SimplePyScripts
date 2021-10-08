#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://core.telegram.org/bots#deep-linking
# SOURCE: https://github.com/python-telegram-bot/python-telegram-bot/wiki/Types-Of-Handlers#deep-linking-start-parameters


# pip install python-telegram-bot
from telegram import Update
from telegram.ext import MessageHandler, CommandHandler, Filters, CallbackContext

from common import get_logger, log_func, start_bot, run_main


log = get_logger(__file__)


@log_func(log)
def on_start(update: Update, context: CallbackContext):
    start_argument = ''
    if context.args:
        # https://t.me/<bot>?start=<start_argument>
        start_argument = context.args[0]

    update.message.reply_text(
        'Start argument: ' + start_argument
    )


@log_func(log)
def on_request(update: Update, context: CallbackContext):
    message = update.message

    message.reply_text(
        message.text
    )


def main():
    handlers = [
        CommandHandler('start', on_start),
        MessageHandler(Filters.text, on_request),
    ]
    start_bot(log, handlers)


if __name__ == '__main__':
    run_main(main, log)
