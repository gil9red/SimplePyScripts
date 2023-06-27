#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys

# pip install python-telegram-bot
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    MessageHandler,
    CommandHandler,
    Filters,
    CallbackContext,
    CallbackQueryHandler,
)

# https://github.com/unmonoqueteclea/calendar-telegram
import telegramcalendar

sys.path.append("..")
from common import get_logger, log_func, reply_error, start_bot, run_main


log = get_logger(__file__)


@log_func(log)
def on_request(update: Update, _: CallbackContext):
    message = update.effective_message

    message.reply_text("Use: /calendar")


@log_func(log)
def on_calendar(update: Update, _: CallbackContext):
    update.effective_message.reply_text(
        "Please select a date: ", reply_markup=telegramcalendar.create_calendar()
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
            reply_markup=ReplyKeyboardRemove(),
        )


def main():
    handlers = [
        CommandHandler("start", on_request),
        CommandHandler("calendar", on_calendar),
        CallbackQueryHandler(on_callback_query),
        MessageHandler(Filters.text, on_request),
    ]
    start_bot(log, handlers)


if __name__ == "__main__":
    run_main(main, log)
