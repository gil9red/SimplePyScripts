#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys

# pip install python-telegram-bot
from telegram import Update, ParseMode
from telegram.ext import MessageHandler, CommandHandler, Filters, CallbackContext, CallbackQueryHandler

# pip install python-telegram-bot-pagination
from telegram_bot_pagination import InlineKeyboardPaginator

sys.path.append('..')

from common import get_logger, log_func, start_bot, run_main
from utils import is_equal_inline_keyboards
from data import character_pages


log = get_logger(__file__)


@log_func(log)
def on_request(update: Update, context: CallbackContext):
    message = update.message

    paginator = InlineKeyboardPaginator(
        page_count=len(character_pages),
        current_page=1,
        data_pattern='character#{page}'
    )

    character = character_pages[0]

    message.reply_text(
        text='*{title}*\n{description}'.format(**character),
        reply_markup=paginator.markup,
        parse_mode=ParseMode.MARKDOWN
    )


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

    query.message.edit_text(
        text='*{title}*\n{description}'.format(**character),
        reply_markup=paginator.markup,
        parse_mode=ParseMode.MARKDOWN
    )


def main():
    handlers = [
        CommandHandler('start', on_request),
        MessageHandler(Filters.text, on_request),
        CallbackQueryHandler(on_callback_query, pattern='^character#'),
    ]
    start_bot(log, handlers)


if __name__ == '__main__':
    run_main(main, log)
