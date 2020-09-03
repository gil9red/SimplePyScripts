#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
import time
import sys

# pip install python-telegram-bot
from telegram import Update, ParseMode, InputMediaPhoto
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackContext, CallbackQueryHandler
from telegram.ext.dispatcher import run_async

# pip install python-telegram-bot-pagination
from telegram_bot_pagination import InlineKeyboardPaginator

sys.path.append('..')

import config
from common import get_logger, log_func, reply_error
from utils import is_equal_inline_keyboards
from data import character_pages


log = get_logger(__file__)


@run_async
@log_func(log)
def on_request(update: Update, context: CallbackContext):
    message = update.message

    paginator = InlineKeyboardPaginator(
        page_count=len(character_pages),
        current_page=1,
        data_pattern='character#{page}'
    )

    character = character_pages[0]

    message.reply_photo(
        photo=open(character['image'], 'rb'),
        caption="*{title}*".format(**character),
        reply_markup=paginator.markup,
        parse_mode=ParseMode.MARKDOWN
    )


@run_async
@log_func(log)
def on_callback_query(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    source, page = query.data.split('#', 1)
    page = int(page)

    paginator = InlineKeyboardPaginator(
        page_count=len(character_pages),
        current_page=page,
        data_pattern=source + '#{page}'
    )

    # Fix error: "telegram.error.BadRequest: Message is not modified"
    if is_equal_inline_keyboards(paginator, query.message.reply_markup):
        return

    character = character_pages[page - 1]

    query.message.edit_media(
        media=InputMediaPhoto(
            media=open(character['image'], 'rb'),
            caption="*{title}*".format(**character),
            parse_mode=ParseMode.MARKDOWN
        ),
        reply_markup=paginator.markup
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

    dp.add_handler(CommandHandler('start', on_request))
    dp.add_handler(MessageHandler(Filters.text, on_request))
    dp.add_handler(CallbackQueryHandler(on_callback_query, pattern='^character#'))

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
