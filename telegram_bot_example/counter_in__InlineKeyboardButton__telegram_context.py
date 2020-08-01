#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
from pathlib import Path

# pip install python-telegram-bot
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackContext, CallbackQueryHandler
from telegram.ext.dispatcher import run_async

import config
from common import get_logger, log_func


log = get_logger(str(Path(__file__)) + '.log')


DATA_TEMPLATE = {
    'number_1': 0,
    'number_2': 0,
    'number_3': 0,
}


@run_async
@log_func(log)
def on_start(update: Update, context: CallbackContext):
    update.message.reply_text('Введите что-нибудь')


@run_async
@log_func(log)
def on_work(update: Update, context: CallbackContext):
    keyboard = []
    for i, (data, value) in enumerate(DATA_TEMPLATE.items()):
        if i % 3 == 0:
            keyboard.append([])
        button = InlineKeyboardButton(str(value), callback_data=data)
        keyboard[-1].append(button)

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        'Ok',
        reply_markup=reply_markup
    )


@run_async
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


def error_callback(update: Update, context: CallbackContext):
    log.exception('Error: %s\nUpdate: %s', context.error, update)
    update.message.reply_text(config.ERROR_TEXT)


def main():
    cpu_count = os.cpu_count()
    workers = cpu_count
    log.debug('System: CPU_COUNT=%s, WORKERS=%s', cpu_count, workers)

    log.debug('Start')

    # Create the EventHandler and pass it your bot's token.
    updater = Updater(
        config.TOKEN,
        workers=workers,
        use_context=True
    )

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', on_start))
    dp.add_handler(MessageHandler(Filters.text, on_work))
    dp.add_handler(CallbackQueryHandler(on_callback_query))

    # log all errors
    dp.add_error_handler(error_callback)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

    log.debug('Finish')


if __name__ == '__main__':
    while True:
        try:
            main()
        except:
            log.exception('')
