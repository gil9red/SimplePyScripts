#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os

# pip install python-telegram-bot
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackContext, CallbackQueryHandler

import config
from common import get_logger, log_func, reply_error, run_main


log = get_logger(__file__)


DATA_TEMPLATE = {
    'number_1': 0,
    'number_2': 0,
    'number_3': 0,
}


@log_func(log)
def on_start(update: Update, context: CallbackContext):
    update.message.reply_text('Write something')


@log_func(log)
def on_request(update: Update, context: CallbackContext):
    keyboard = [[
        InlineKeyboardButton(str(value), callback_data=data)
        for data, value in DATA_TEMPLATE.items()
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        'Ok',
        reply_markup=reply_markup
    )


@log_func(log)
def on_callback_query(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    # Change counter from telegram buttons context
    inline_keyboard = query.message.reply_markup.inline_keyboard
    for rows in inline_keyboard:
        for x in rows:
            if x.callback_data == query.data:
                x.text = str(int(x.text) + 1)

    reply_markup = InlineKeyboardMarkup(inline_keyboard)

    query.message.edit_reply_markup(reply_markup=reply_markup)


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
    dp.add_handler(CallbackQueryHandler(on_callback_query, run_async=True))

    dp.add_error_handler(on_error)

    updater.start_polling()
    updater.idle()

    log.debug('Finish')


if __name__ == '__main__':
    run_main(main, log)
