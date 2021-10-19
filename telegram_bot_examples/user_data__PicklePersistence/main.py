#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys

# pip install python-telegram-bot
from telegram import Update
from telegram.ext import MessageHandler, CommandHandler, Filters, CallbackContext, PicklePersistence

sys.path.append('..')
from common import get_logger, log_func, reply_error, start_bot, run_main


log = get_logger(__file__)


@log_func(log)
def on_start(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        'Commands: set and get.'
    )


@log_func(log)
def on_set(update: Update, context: CallbackContext):
    message = update.effective_message

    end = context.match.span()[1]
    text = message.text[end:].strip()

    context.user_data['text'] = text

    message.reply_text('Saving!')


@log_func(log)
def on_get(update: Update, context: CallbackContext):
    message = update.effective_message

    text = context.user_data.get('text', '<Not data, using command set>')

    message.reply_text(
        "get: " + text
    )


@log_func(log)
def on_request(update: Update, context: CallbackContext):
    message = update.effective_message

    message.reply_text(
        'Echo: ' + message.text
    )


def main():
    handlers = [
        CommandHandler('start', on_start),
        MessageHandler(Filters.regex(r'(?i)^(set)\b'), on_set),
        MessageHandler(Filters.regex(r'(?i)^get'), on_get),
        MessageHandler(Filters.text, on_request),
    ]

    start_bot(
        log,
        handlers,
        persistence=PicklePersistence(filename='data.pickle')
    )


if __name__ == '__main__':
    run_main(main, log)
