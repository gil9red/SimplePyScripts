#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install python-telegram-bot
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import MessageHandler, CommandHandler, Filters, CallbackContext, CallbackQueryHandler

from common import get_logger, log_func, start_bot, run_main


log = get_logger(__file__)


DATA_TEMPLATE = {
    'number_1': 0,
    'number_2': 0,
    'number_3': 0,
}


@log_func(log)
def on_start(update: Update, context: CallbackContext):
    update.effective_message.reply_text('Write something')


@log_func(log)
def on_request(update: Update, context: CallbackContext):
    keyboard = [[
        InlineKeyboardButton(str(value), callback_data=data)
        for data, value in DATA_TEMPLATE.items()
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.effective_message.reply_text(
        'Ok',
        reply_markup=reply_markup
    )


@log_func(log)
def on_callback_query(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    reply_markup = query.message.reply_markup

    # Change counter from telegram buttons context
    inline_keyboard = reply_markup.inline_keyboard
    for rows in inline_keyboard:
        for x in rows:
            if x.callback_data == query.data:
                x.text = str(int(x.text) + 1)

    query.message.edit_reply_markup(reply_markup=reply_markup)


def main():
    handlers = [
        CommandHandler('start', on_start),
        MessageHandler(Filters.text, on_request),
        CallbackQueryHandler(on_callback_query),
    ]
    start_bot(log, handlers)


if __name__ == '__main__':
    run_main(main, log)
