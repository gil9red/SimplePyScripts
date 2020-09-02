#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys

# pip install python-telegram-bot
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

# https://github.com/unmonoqueteclea/calendar-telegram
import telegramcalendar

sys.path.append('..')
import config


def on_calendar(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Please select a date: ",
        reply_markup=telegramcalendar.create_calendar()
    )


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


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(
        config.TOKEN,
        use_context=True
    )

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('calendar', on_calendar))
    dp.add_handler(CallbackQueryHandler(on_callback_query))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
