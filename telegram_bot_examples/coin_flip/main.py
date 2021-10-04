#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
import time
import sys
import random
import re

# pip install python-telegram-bot
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackContext, CallbackQueryHandler
from telegram.ext.dispatcher import run_async

sys.path.append('..')
import config
from common import get_logger, log_func, reply_error, fill_string_pattern


PATTERN_COIN_FLIP = re.compile(r'^coin_flip$')
PATTERN_HIDE_COIN_FLIP = re.compile(r'^hide_coin_flip$')

COIN_VARIANTS = {
    'орел': 'орел_512x512.png',
    'решка': 'решка_512x512.png',
}


log = get_logger(__file__)


@run_async
@log_func(log)
def on_start(update: Update, context: CallbackContext):
    reply_markup = ReplyKeyboardMarkup.from_button(
        'Подкинуть монетку', resize_keyboard=True
    )

    update.effective_message.reply_html(
        'Тыкни на "Подкинуть монетку" :)',
        reply_markup=reply_markup,
    )


@run_async
@log_func(log)
def on_request(update: Update, context: CallbackContext):
    message = update.effective_message

    reply_markup = InlineKeyboardMarkup.from_button(
        InlineKeyboardButton("Бросить монету", callback_data=fill_string_pattern(PATTERN_COIN_FLIP))
    )

    message.reply_text(
        'Подкинуть монету?',
        reply_markup=reply_markup,
    )


@run_async
@log_func(log)
def on_callback_coin_flip(update: Update, context: CallbackContext):
    message = update.effective_message

    query = update.callback_query
    query.answer()

    reply_markup = InlineKeyboardMarkup.from_row([
        InlineKeyboardButton('🔁 Повторить', callback_data=fill_string_pattern(PATTERN_COIN_FLIP)),
        InlineKeyboardButton('❌ Убрать', callback_data=fill_string_pattern(PATTERN_HIDE_COIN_FLIP)),
    ])

    value = random.choice(list(COIN_VARIANTS))
    f = open(COIN_VARIANTS[value], 'rb')

    is_new = not message.photo
    if is_new:
        message.reply_photo(
            f,
            caption=f"🍀 Бросок: {value}",
            reply_markup=reply_markup,
            quote=True
        )
    else:
        message.edit_media(
            InputMediaPhoto(f, f'{message.caption}, {value}'),
            reply_markup=reply_markup
        )


@run_async
@log_func(log)
def on_callback_hide_coin_flip(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    query.message.delete()


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

    dp.add_handler(CallbackQueryHandler(on_callback_coin_flip, pattern=PATTERN_COIN_FLIP))
    dp.add_handler(CallbackQueryHandler(on_callback_hide_coin_flip, pattern=PATTERN_HIDE_COIN_FLIP))

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
