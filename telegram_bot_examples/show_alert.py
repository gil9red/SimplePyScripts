#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
import time

# pip install python-telegram-bot
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackContext, CallbackQueryHandler

import config
from common import get_logger, log_func, reply_error


log = get_logger(__file__)


@log_func(log)
def on_start(update: Update, context: CallbackContext):
    reply_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("dog", callback_data='dog'),
            InlineKeyboardButton("cat", callback_data='cat'),
            InlineKeyboardButton("other", callback_data='other'),
        ],
    ])

    update.effective_message.reply_text(
        f'Hello {update.message.chat.first_name}!', reply_markup=reply_markup
    )


@log_func(log)
def on_request(update: Update, context: CallbackContext):
    message = update.effective_message

    message.reply_text(
        'Echo: ' + message.text
    )


@log_func(log)
def on_select(update, context):
    query = update.callback_query

    if query.data == 'cat':
        query.answer(text='You chose cat!', show_alert=True)
    elif query.data == 'dog':
        query.answer(text='You chose dog!', show_alert=True)
    else:
        query.answer('Nothing')


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
    dp.add_handler(CallbackQueryHandler(on_select, run_async=True))

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
