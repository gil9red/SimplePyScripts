#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys
import random
import re

# pip install python-telegram-bot
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from telegram.ext import MessageHandler, CommandHandler, Filters, CallbackContext, CallbackQueryHandler

sys.path.append('..')
from common import get_logger, log_func, fill_string_pattern, start_bot, run_main


PATTERN_COIN_FLIP = re.compile(r'^coin_flip$')
PATTERN_HIDE_COIN_FLIP = re.compile(r'^hide_coin_flip$')

COIN_VARIANTS = {
    'орел': 'орел_512x512.png',
    'решка': 'решка_512x512.png',
}


log = get_logger(__file__)


@log_func(log)
def on_start(update: Update, context: CallbackContext):
    reply_markup = ReplyKeyboardMarkup.from_button(
        'Подкинуть монетку', resize_keyboard=True
    )

    update.effective_message.reply_html(
        'Тыкни на "Подкинуть монетку" :)',
        reply_markup=reply_markup,
    )


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


@log_func(log)
def on_callback_hide_coin_flip(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    query.message.delete()


def main():
    handlers = [
        CommandHandler('start', on_start),
        MessageHandler(Filters.text, on_request),
        CallbackQueryHandler(on_callback_coin_flip, pattern=PATTERN_COIN_FLIP),
        CallbackQueryHandler(on_callback_hide_coin_flip, pattern=PATTERN_HIDE_COIN_FLIP),
    ]
    start_bot(log, handlers)


if __name__ == '__main__':
    run_main(main, log)
