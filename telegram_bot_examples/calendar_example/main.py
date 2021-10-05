#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
import sys

# pip install python-telegram-bot
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackContext, CallbackQueryHandler

# https://github.com/unmonoqueteclea/calendar-telegram
import telegramcalendar

sys.path.append('..')
import config
from common import get_logger, log_func, reply_error, run_main


log = get_logger(__file__)


@log_func(log)
def on_start(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Write something'
    )


@log_func(log)
def on_request(update: Update, context: CallbackContext):
    message = update.message

    message.reply_text(
        'Echo: ' + message.text
    )


@log_func(log)
def on_calendar(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Please select a date: ",
        reply_markup=telegramcalendar.create_calendar()
    )


@log_func(log)
def on_callback_query(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    bot = context.bot

    selected, date = telegramcalendar.process_calendar_selection(bot, update)
    if selected:
        query.message.reply_text(
            text="You selected %s" % (date.strftime("%d/%m/%Y")),
            reply_markup=ReplyKeyboardRemove()
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
    dp.add_handler(CommandHandler('calendar', on_calendar, run_async=True))
    dp.add_handler(CallbackQueryHandler(on_callback_query, run_async=True))
    dp.add_handler(MessageHandler(Filters.text, on_request, run_async=True))

    dp.add_error_handler(on_error)

    updater.start_polling()
    updater.idle()

    log.debug('Finish')


if __name__ == '__main__':
    run_main(main, log)
