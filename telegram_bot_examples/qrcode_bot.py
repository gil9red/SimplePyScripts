#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
from io import BytesIO

# pip install python-telegram-bot
from telegram import Update
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackContext

# pip install qrcode
import qrcode

import config
from common import get_logger, log_func, reply_error, run_main


log = get_logger(__file__)


@log_func(log)
def on_start(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        'Write something'
    )


@log_func(log)
def on_request(update: Update, context: CallbackContext):
    message = update.effective_message

    bytes_io = BytesIO()

    img = qrcode.make(message.text)
    img.save(bytes_io, format='PNG')

    # После выполнения save внутренний указатель будет в конце данных,
    # а для работы с bytes_io нужно вернуть в начало
    bytes_io.seek(0)

    message.reply_photo(photo=bytes_io, quote=True)


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

    dp.add_handler(CommandHandler('start', on_start, run_async=True))
    dp.add_handler(MessageHandler(Filters.text, on_request, run_async=True))

    dp.add_error_handler(on_error)

    updater.start_polling()
    updater.idle()

    log.debug('Finish')


if __name__ == '__main__':
    run_main(main, log)
