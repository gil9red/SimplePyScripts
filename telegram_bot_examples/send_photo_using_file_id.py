#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://core.telegram.org/bots/api#sendphoto
#         https://core.telegram.org/bots/api#photosize
#         https://core.telegram.org/bots/api#sending-files


import os
import time

# pip install python-telegram-bot
from telegram import Update
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackContext
from telegram.ext.dispatcher import run_async

import config
from common import get_logger, log_func, reply_error


log = get_logger(__file__)


@run_async
@log_func(log)
def on_start(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        'Отправка картинки боту вернет её с file_id\n'
        'Отправка текстом file_id вернет картинку'
    )


@run_async
@log_func(log)
def on_request(update: Update, context: CallbackContext):
    message = update.effective_message
    file_id = message.text

    try:
        message.reply_photo(file_id, quote=True)
    except Exception as e:
        message.reply_text(f'Error: {e}')
        raise e


@run_async
@log_func(log)
def on_photo(update: Update, context: CallbackContext):
    message = update.effective_message

    photo_large = max(message.photo, key=lambda x: (x.width, x.height))
    file_id = photo_large.file_id

    message.reply_photo(
        file_id,
        caption=f'file_id: {file_id}',
        quote=True
    )


def on_error(update: Update, context: CallbackContext):
    reply_error(log, update, context)


def main():
    cpu_count = os.cpu_count()
    workers = cpu_count
    log.debug('System: CPU_COUNT=%s, WORKERS=%s', cpu_count, workers)

    log.debug('Start')

    updater = Updater(
        config.TOKEN,
        workers=workers,
        use_context=True
    )

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', on_start))
    dp.add_handler(MessageHandler(Filters.text, on_request))
    dp.add_handler(MessageHandler(Filters.photo, on_photo))

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
