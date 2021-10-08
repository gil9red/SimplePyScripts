#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install python-telegram-bot
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import MessageHandler, CommandHandler, Filters, CallbackContext

from common import get_logger, log_func, start_bot, run_main


contact_keyboard = KeyboardButton('Send contact', request_contact=True)
location_keyboard = KeyboardButton('Send location', request_location=True)
custom_keyboard = [[contact_keyboard, location_keyboard]]
REPLY_KEYBOARD_MARKUP = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)


log = get_logger(__file__)


@log_func(log)
def on_start(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Write something',
        reply_markup=REPLY_KEYBOARD_MARKUP
    )


@log_func(log)
def on_request(update: Update, context: CallbackContext):
    message = update.message

    message.reply_text(
        'Echo: ' + message.text,
        reply_markup=REPLY_KEYBOARD_MARKUP
    )


@log_func(log)
def on_contact_or_location(update: Update, context: CallbackContext):
    message = update.message

    text = ''
    if message.contact:
        text += str(message.contact)

    if message.location:
        text += str(message.location)

    message.reply_text(
        text,
        reply_markup=REPLY_KEYBOARD_MARKUP
    )


def main():
    handlers = [
        CommandHandler('start', on_start),
        MessageHandler(Filters.text, on_request),
        MessageHandler(Filters.contact | Filters.location, on_contact_or_location),
    ]
    start_bot(log, handlers)


if __name__ == '__main__':
    run_main(main, log)
