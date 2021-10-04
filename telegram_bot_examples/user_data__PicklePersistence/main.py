#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
import time
import sys

# pip install python-telegram-bot
from telegram import Update
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackContext, PicklePersistence

sys.path.append('..')

import config
from common import get_logger, log_func, reply_error


log = get_logger(__file__)


@log_func(log)
def on_start(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Commands: set and get.'
    )


@log_func(log)
def on_set(update: Update, context: CallbackContext):
    message = update.message

    end = context.match.span()[1]
    text = message.text[end:].strip()

    context.user_data['text'] = text

    message.reply_text('Saving!')


@log_func(log)
def on_get(update: Update, context: CallbackContext):
    message = update.message

    text = context.user_data.get('text', '<Not data, using command set>')

    message.reply_text(
        "get: " + text
    )


@log_func(log)
def on_request(update: Update, context: CallbackContext):
    message = update.message

    message.reply_text(
        'Echo: ' + message.text
    )


def on_error(update: Update, context: CallbackContext):
    reply_error(log, update, context)


def main():
    cpu_count = os.cpu_count()
    workers = cpu_count
    log.debug('System: CPU_COUNT=%s, WORKERS=%s', cpu_count, workers)

    log.debug('Start')

    persistence = PicklePersistence(filename='data.pickle')

    updater = Updater(
        config.TOKEN,
        workers=workers,
        persistence=persistence,
        use_context=True
    )

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', on_start, run_async=True))
    dp.add_handler(MessageHandler(Filters.regex(r'(?i)^(set)\b'), on_set, run_async=True))
    dp.add_handler(MessageHandler(Filters.regex(r'(?i)^get'), on_get, run_async=True))
    dp.add_handler(MessageHandler(Filters.text, on_request, run_async=True))

    dp.add_error_handler(on_error)

    updater.start_polling()
    updater.idle()

    log.debug('Finish')


if __name__ == '__main__':
    while True:
        try:
            main()
        except:
            log.exception('')

            timeout = 15
            log.info(f'Restarting the bot after {timeout} seconds')
            time.sleep(timeout)
