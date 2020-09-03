#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
import time
import sys

# pip install python-telegram-bot
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackContext, CallbackQueryHandler
from telegram.ext.dispatcher import run_async

# https://github.com/unmonoqueteclea/calendar-telegram
import telegramcalendar

sys.path.append('..')
import config
from common import get_logger, log_func, reply_error


log = get_logger(__file__)


@run_async
@log_func(log)
def on_start(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Введите что-нибудь'
    )


@run_async
@log_func(log)
def on_request(update: Update, context: CallbackContext):
    message = update.message

    message.reply_text(
        'Echo: ' + message.text
    )


@run_async
@log_func(log)
def on_calendar(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Please select a date: ",
        reply_markup=telegramcalendar.create_calendar()
    )


@run_async
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

    # Create the EventHandler and pass it your bot's token.
    updater = Updater(
        config.TOKEN,
        workers=workers,
        use_context=True
    )

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', on_start))
    dp.add_handler(CommandHandler('calendar', on_calendar))
    dp.add_handler(CallbackQueryHandler(on_callback_query))
    dp.add_handler(MessageHandler(Filters.text, on_request))

    # Handle all errors
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
