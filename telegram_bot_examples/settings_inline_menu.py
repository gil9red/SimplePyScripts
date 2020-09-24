#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import enum
import os
import time
import re

# pip install python-telegram-bot
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater, MessageHandler, CommandHandler, Filters, CallbackContext, CallbackQueryHandler
)
from telegram.ext.dispatcher import run_async

import config
from common import get_logger, log_func, reply_error


def is_equal_inline_keyboards(keyboard_1: InlineKeyboardMarkup, keyboard_2: InlineKeyboardMarkup) -> bool:
    keyboard_1 = keyboard_1.to_dict()['inline_keyboard']
    keyboard_2 = keyboard_2.to_dict()['inline_keyboard']
    return keyboard_1 == keyboard_2


class SettingState(enum.Enum):
    DEBUG = ['On', 'Off']
    YEAR = {
        '2020': False, '2019': False, '2018': False, '2017': False,
        '2016': False, '2015': False, '2014': False, '2013': False,
    }
    SEX = ['Male', 'Female']

    MAIN = enum.auto()
    
    def get_callback_data(self) -> str:
        return str(self).replace('.', '_')

    def get_pattern_with_params(self) -> re.Pattern:
        return re.compile('^' + self.get_callback_data() + '_(.+)$')

    def get_pattern_full(self) -> re.Pattern:
        return re.compile(
            '^' + self.get_callback_data() + '$|' + self.get_pattern_with_params().pattern
        )


CHECKBOX = '✅'
CHECKBOX_EMPTY = '⬜'
RADIOBUTTON = '🟢'
RADIOBUTTON_EMPTY = '⚪'

INLINE_KEYBOARD_BUTTON_BACK = InlineKeyboardButton(
    "<back>", callback_data=SettingState.MAIN.get_callback_data()
)


def _on_reply_debug(update: Update, context: CallbackContext):
    query = update.callback_query

    settings = SettingState.DEBUG
    data = settings.get_callback_data()
    pattern = settings.get_pattern_with_params()

    m = pattern.search(query.data)
    if m:
        context.user_data[settings] = m.group(1)

    debug = context.user_data.get(settings, 'Off')

    buttons = [
        InlineKeyboardButton(
            (RADIOBUTTON if debug == value else RADIOBUTTON_EMPTY) + ' ' + value,
            callback_data=data + '_' + value
        )
        for value in settings.value
    ]

    reply_markup = InlineKeyboardMarkup([
        buttons,
        [INLINE_KEYBOARD_BUTTON_BACK]
    ])

    # Fix error: "telegram.error.BadRequest: Message is not modified"
    if is_equal_inline_keyboards(reply_markup, query.message.reply_markup):
        return

    text = f'Selecting {settings.name}:'
    query.edit_message_text(text, reply_markup=reply_markup)


def _on_reply_year(update: Update, context: CallbackContext):
    query = update.callback_query

    settings = SettingState.YEAR
    data = settings.get_callback_data()

    if settings not in context.user_data:
        context.user_data[settings] = dict(settings.value)

    data_year = context.user_data[settings]

    pattern = settings.get_pattern_with_params()

    m = pattern.search(query.data)
    if m:
        year = m.group(1)
        if year not in data_year:
            return

        data_year[year] = not data_year[year]

    keys = list(settings.value)

    buttons = []
    for i in range(0, len(keys), 4):
        row = []
        for key in keys[i: i + 4]:
            value = data_year[key]

            row.append(
                InlineKeyboardButton(
                    (CHECKBOX if value else CHECKBOX_EMPTY) + ' ' + key,
                    callback_data=data + '_' + key
                )
            )

        buttons.append(row)

    buttons.append([INLINE_KEYBOARD_BUTTON_BACK])

    reply_markup = InlineKeyboardMarkup(buttons)

    # Fix error: "telegram.error.BadRequest: Message is not modified"
    if is_equal_inline_keyboards(reply_markup, query.message.reply_markup):
        return

    text = f'Selecting {settings.name}:'
    query.edit_message_text(text, reply_markup=reply_markup)


def _on_reply_sex(update: Update, context: CallbackContext):
    query = update.callback_query

    settings = SettingState.SEX
    data = settings.get_callback_data()
    pattern = settings.get_pattern_with_params()

    m = pattern.search(query.data)
    if m:
        context.user_data[settings] = m.group(1)

    sex = context.user_data.get(settings, 'Male')

    buttons = [
        InlineKeyboardButton(
            (RADIOBUTTON if sex == value else RADIOBUTTON_EMPTY) + ' ' + value,
            callback_data=data + '_' + value
        )
        for value in settings.value
    ]

    reply_markup = InlineKeyboardMarkup([
        buttons,
        [INLINE_KEYBOARD_BUTTON_BACK]
    ])

    # Fix error: "telegram.error.BadRequest: Message is not modified"
    if is_equal_inline_keyboards(reply_markup, query.message.reply_markup):
        return

    text = f'Selecting {settings.name}:'
    query.edit_message_text(text, reply_markup=reply_markup)


log = get_logger(__file__)


@run_async
@log_func(log)
def on_start(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Enter /settings'
    )


@run_async
@log_func(log)
def on_settings(update: Update, context: CallbackContext):
    # Если функция вызвана из CallbackQueryHandler
    query = update.callback_query
    if query:
        query.answer()

    message = update.effective_message

    reply_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(SettingState.DEBUG.name, callback_data=SettingState.DEBUG.get_callback_data()),
            InlineKeyboardButton(SettingState.YEAR.name, callback_data=SettingState.YEAR.get_callback_data()),
            InlineKeyboardButton(SettingState.SEX.name, callback_data=SettingState.SEX.get_callback_data()),
        ]
    ])

    text = 'Selecting settings:'

    if query:
        message.edit_text(text, reply_markup=reply_markup)
    else:
        message.reply_text(text, reply_markup=reply_markup)


@run_async
@log_func(log)
def on_debug(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    _on_reply_debug(update, context)


@run_async
@log_func(log)
def on_year(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    _on_reply_year(update, context)


@run_async
@log_func(log)
def on_sex(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    _on_reply_sex(update, context)


@run_async
@log_func(log)
def on_request(update: Update, context: CallbackContext):
    message = update.message

    message.reply_text(
        'Echo: ' + message.text
    )


def on_error(update: Update, context: CallbackContext):
    reply_error(log, update, context)


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

    dp.add_handler(CommandHandler('settings', on_settings))
    dp.add_handler(CallbackQueryHandler(on_settings, pattern=SettingState.MAIN.get_pattern_full()))

    dp.add_handler(CallbackQueryHandler(on_debug, pattern=SettingState.DEBUG.get_pattern_full()))
    dp.add_handler(CallbackQueryHandler(on_year, pattern=SettingState.YEAR.get_pattern_full()))
    dp.add_handler(CallbackQueryHandler(on_sex, pattern=SettingState.SEX.get_pattern_full()))

    dp.add_handler(MessageHandler(Filters.text, on_request))

    dp.add_error_handler(on_error)

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

            timeout = 15
            log.info(f'Restarting the bot after {timeout} seconds')
            time.sleep(timeout)
