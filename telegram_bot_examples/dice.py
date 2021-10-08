#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import re

# pip install python-telegram-bot
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Dice
from telegram.ext import CommandHandler, CallbackContext, CallbackQueryHandler

from common import get_logger, log_func, start_bot, run_main


log = get_logger(__file__)


PATTERN_DICE = re.compile("^DICE_(" + "|".join(Dice.ALL_EMOJI) + ")$")

REPLY_MARKUP = InlineKeyboardMarkup.from_row([
    InlineKeyboardButton(text=x, callback_data="DICE_" + x) for x in Dice.ALL_EMOJI
])


@log_func(log)
def on_start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Select dice:",
        reply_markup=REPLY_MARKUP
    )


@log_func(log)
def on_callback_query_dice(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    emoji = PATTERN_DICE.search(query.data).group(1)

    rs_message = query.message.reply_dice(emoji=emoji, reply_markup=REPLY_MARKUP)
    query.message.reply_text(f'dice={rs_message.dice.value}')


def main():
    handlers = [
        CommandHandler('start', on_start),
        CallbackQueryHandler(on_callback_query_dice, pattern=PATTERN_DICE),
    ]
    start_bot(log, handlers)


if __name__ == '__main__':
    run_main(main, log)
