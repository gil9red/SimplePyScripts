#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import threading

# pip install python-telegram-bot
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    MessageHandler,
    CommandHandler,
    Filters,
    CallbackContext,
    CallbackQueryHandler,
)

from common import get_logger, log_func, start_bot, run_main


log = get_logger(__file__)


lock = threading.Lock()
DATA_TEMPLATE = {
    "number_1": 0,
    "number_2": 0,
    "number_3": 0,
}

# chat_id -> message_id -> DATA_TEMPLATE
CACHE_NUMBERS: dict[int, dict[int, dict[str, int]]] = dict()


def get_reply_markup(data: dict[str, int]) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(str(value), callback_data=data)
            for data, value in data.items()
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


@log_func(log)
def on_start(update: Update, _: CallbackContext):
    update.effective_message.reply_text("Write something")


@log_func(log)
def on_request(update: Update, _: CallbackContext):
    chat_id = update.effective_chat.id
    message_id = update.effective_message.message_id

    if chat_id not in CACHE_NUMBERS:
        CACHE_NUMBERS[chat_id] = dict()
    if message_id not in CACHE_NUMBERS[chat_id]:
        CACHE_NUMBERS[chat_id][message_id] = DATA_TEMPLATE.copy()

    data = CACHE_NUMBERS[chat_id][message_id]

    update.effective_message.reply_text("Ok", reply_markup=get_reply_markup(data))


@log_func(log)
def on_callback_query(update: Update, _: CallbackContext):
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

    query.message.edit_reply_markup(reply_markup=get_reply_markup(data))


def main():
    handlers = [
        CommandHandler("start", on_start),
        MessageHandler(Filters.text, on_request),
        CallbackQueryHandler(on_callback_query),
    ]
    start_bot(log, handlers)


if __name__ == "__main__":
    run_main(main, log)
