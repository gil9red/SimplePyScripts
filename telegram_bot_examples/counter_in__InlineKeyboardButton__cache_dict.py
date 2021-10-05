#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
import time
from typing import Dict
import threading

# pip install python-telegram-bot
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackContext, CallbackQueryHandler

import config
from common import get_logger, log_func, reply_error


log = get_logger(__file__)


lock = threading.Lock()
DATA_TEMPLATE = {
    'number_1': 0,
    'number_2': 0,
    'number_3': 0,
}

# chat_id -> message_id -> DATA_TEMPLATE
CACHE_NUMBERS: Dict[int, Dict[int, Dict[str, int]]] = dict()


def get_reply_markup(data: Dict[str, int]) -> InlineKeyboardMarkup:
    keyboard = [[
        InlineKeyboardButton(str(value), callback_data=data)
        for data, value in data.items()
    ]]
    return InlineKeyboardMarkup(keyboard)


@log_func(log)
def on_start(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        'Write something'
    )


@log_func(log)
def on_request(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message_id = update.message.message_id

    if chat_id not in CACHE_NUMBERS:
        CACHE_NUMBERS[chat_id] = dict()
    if message_id not in CACHE_NUMBERS[chat_id]:
        CACHE_NUMBERS[chat_id][message_id] = DATA_TEMPLATE.copy()

    data = CACHE_NUMBERS[chat_id][message_id]

    update.message.reply_text(
        'Ok',
        reply_markup=get_reply_markup(data)
    )


@log_func(log)
def on_callback_query(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    chat_id = query.message.chat_id
    message_id = query.message.message_id

    # Restore from inline keyboard of message
    if chat_id not in CACHE_NUMBERS:
        CACHE_NUMBERS[chat_id] = dict()

    if message_id not in CACHE_NUMBERS[chat_id]:
        inline_keyboard = query.message.reply_markup.inline_keyboard
        data = dict()
        for rows in inline_keyboard:
            for x in rows:
                data[x.callback_data] = int(x.text)
        CACHE_NUMBERS[chat_id][message_id] = data

    data = CACHE_NUMBERS[chat_id][message_id]

    with lock:
        data[query.data] += 1

    query.message.edit_reply_markup(
        reply_markup=get_reply_markup(data)
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

    dp.add_handler(CommandHandler('start', on_start, run_async=True))
    dp.add_handler(MessageHandler(Filters.text, on_request, run_async=True))
    dp.add_handler(CallbackQueryHandler(on_callback_query, run_async=True))

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
