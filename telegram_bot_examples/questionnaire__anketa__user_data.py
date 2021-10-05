#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os

# pip install python-telegram-bot
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackContext

import config
from common import get_logger, log_func, reply_error, run_main


BUTTON_START_ANKETA = 'Заполнить анкету'
REPLY_KEYBOARD_MARKUP = ReplyKeyboardMarkup(
    [[BUTTON_START_ANKETA]], resize_keyboard=True
)
REPLY_KEYBOARD_MARKUP_SET_RATING = ReplyKeyboardMarkup(
    [["1", "2", "3", "4", "5"]],
    resize_keyboard=True, one_time_keyboard=True
)

STATE_USER_NAME = 'user_name'
STATE_USER_AGE = 'user_age'
STATE_RATING = 'rating'
STATE_COMMENT = 'comment'

SKIP = "Пропустить"

ANKETA_TEXT_FORMAT = """\
Результат опроса:
    <b>Имя:</b> {name}
    <b>Возраст:</b> {age}
    <b>Оценка:</b> {rating}
    <b>Комментарий:</b> {comment}
"""


log = get_logger(__file__)


@log_func(log)
def on_start(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Введите что-нибудь', reply_markup=REPLY_KEYBOARD_MARKUP
    )


@log_func(log)
def on_request(update: Update, context: CallbackContext):
    message = update.message

    state = context.user_data.get('state')

    if message.text == BUTTON_START_ANKETA or not state:
        context.user_data['state'] = ''
        context.user_data['name'] = ''
        context.user_data['age'] = ''
        context.user_data['rating'] = ''
        context.user_data['comment'] = ''

        update.message.reply_text('Как вас зовут?', reply_markup=ReplyKeyboardRemove())
        context.user_data['state'] = STATE_USER_NAME
        return

    if state == STATE_USER_NAME:
        context.user_data['name'] = message.text
        context.user_data['state'] = STATE_USER_AGE

        message.reply_text("Сколько вам лет?")
        return

    if state == STATE_USER_AGE:
        context.user_data['age'] = message.text
        context.user_data['state'] = STATE_RATING

        message.reply_text(
            "Оцените статью от 1 до 5",
            reply_markup=REPLY_KEYBOARD_MARKUP_SET_RATING
        )
        return

    if state == STATE_RATING:
        context.user_data['rating'] = message.text
        context.user_data['state'] = STATE_COMMENT

        update.message.reply_text(
            "Напишите отзыв или нажмите кнопку пропустить этот шаг.",
            reply_markup=ReplyKeyboardMarkup(
                [[SKIP]],
                resize_keyboard=True, one_time_keyboard=True
            )
        )
        return

    if state == STATE_COMMENT:
        if message.text != SKIP:
            context.user_data['comment'] = message.text
            message.reply_text(
                "Спасибо вам за комментарий!", reply_markup=REPLY_KEYBOARD_MARKUP
            )

        text = ANKETA_TEXT_FORMAT.format(**context.user_data)
        message.reply_html(text)

        message.reply_text("Спасибо!", reply_markup=REPLY_KEYBOARD_MARKUP)


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

    dp.add_error_handler(on_error)

    updater.start_polling()
    updater.idle()

    log.debug('Finish')


if __name__ == '__main__':
    run_main(main, log)
