#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
import time
import re

# pip install python-telegram-bot
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Dice
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
from telegram.ext.dispatcher import run_async

import config
from common import get_logger, log_func, reply_error


log = get_logger(__file__)


PATTERN_DICE = re.compile("^DICE_(" + "|".join(Dice.ALL_EMOJI) + ")$")

REPLY_MARKUP = InlineKeyboardMarkup.from_row([
    InlineKeyboardButton(text=x, callback_data="DICE_" + x) for x in Dice.ALL_EMOJI
])


@run_async
@log_func(log)
def on_start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Select dice:",
        reply_markup=REPLY_MARKUP
    )


@run_async
@log_func(log)
def on_callback_query_dice(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    emoji = PATTERN_DICE.search(query.data).group(1)

    rs_message = query.message.reply_dice(emoji=emoji, reply_markup=REPLY_MARKUP)
    query.message.reply_text('dice=' + str(rs_message.dice.value))


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

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', on_start))
    dp.add_handler(CallbackQueryHandler(on_callback_query_dice, pattern=PATTERN_DICE))

    dp.add_error_handler(on_error)

    updater.start_polling()
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
