#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install python-telegram-bot
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import MessageHandler, CommandHandler, Filters, CallbackContext, CallbackQueryHandler

from common import get_logger, log_func, start_bot, run_main


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
def on_select(update, context):
    query = update.callback_query

    if query.data == 'cat':
        query.answer(text='You chose cat!', show_alert=True)
    elif query.data == 'dog':
        query.answer(text='You chose dog!', show_alert=True)
    else:
        query.answer('Nothing')


def main():
    handlers = [
        CommandHandler('start', on_start),
        MessageHandler(Filters.text, on_start),
        CallbackQueryHandler(on_select),
    ]
    start_bot(log, handlers)


if __name__ == '__main__':
    run_main(main, log)
