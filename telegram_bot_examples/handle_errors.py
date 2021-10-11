#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/python-telegram-bot/python-telegram-bot/blob/bc7c422a11a60a3064601aac3fd5a26fd9b45ae9/examples/errorhandlerbot.py#L28


import enum
import json
import html
import logging
import traceback

# pip install python-telegram-bot
from telegram import Update, ReplyKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, Defaults

import config
from common import log_func, get_logger


MESS_MAX_LENGTH = 4096
DEVELOPER_CHAT_ID = ...


class ErrorHandlingMode(enum.Enum):
    SILENCE = enum.auto()
    SILENCE_WITH_REPORT = enum.auto()
    SHOW_ERROR = enum.auto()
    SHOW_ERROR_WITH_REPORT = enum.auto()


COMMANDS = [x.name for x in ErrorHandlingMode]
REPLY_KEYBOARD_MARKUP = ReplyKeyboardMarkup.from_column(COMMANDS, resize_keyboard=True)

DATA = {
    'MODE': ErrorHandlingMode.SILENCE
}

log = get_logger(__file__)


def reply_error(log: logging.Logger, update: Update, context: CallbackContext):
    log.error('Error: %s\nUpdate: %s', context.error, update, exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)

    # Build the message with some markup and additional information about what happened.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message_report = (
        f'An exception was raised while handling an update\n'
        f'<pre>update = {html.escape(json.dumps(update_str, indent=4, ensure_ascii=False))}</pre>\n'
        f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n'
        f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n'
        f'<pre>{html.escape(tb_string)}</pre>'
    )

    text = html.escape(config.ERROR_TEXT)
    if DATA["MODE"] in [ErrorHandlingMode.SHOW_ERROR, ErrorHandlingMode.SHOW_ERROR_WITH_REPORT]:
        text = f'{text}\n\n{message_report}'

    if update:
        for n in range(0, len(text), MESS_MAX_LENGTH):
            mess = text[n: n + MESS_MAX_LENGTH]
            update.effective_message.reply_html(mess)

    # Finally, send the message
    if DATA["MODE"] in [ErrorHandlingMode.SILENCE_WITH_REPORT, ErrorHandlingMode.SHOW_ERROR_WITH_REPORT]:
        for n in range(0, len(message_report), MESS_MAX_LENGTH):
            mess = message_report[n: n + MESS_MAX_LENGTH]
            context.bot.send_message(chat_id=DEVELOPER_CHAT_ID, text=mess, parse_mode=ParseMode.HTML)


@log_func(log)
def on_request(update: Update, context: CallbackContext):
    message = update.effective_message

    message.reply_text(
        f'Current user id: {message.from_user.id}\n'
        f'Current chat id: {message.chat_id}\n'
        f'Current mode: {DATA["MODE"]}.\nSelect mode and error:',
        reply_markup=REPLY_KEYBOARD_MARKUP
    )


@log_func(log)
def on_reply_command(update: Update, context: CallbackContext):
    message = update.effective_message

    DATA["MODE"] = ErrorHandlingMode[message.text]

    message.reply_text(
        f'You select mode: {DATA["MODE"]}',
        reply_markup=REPLY_KEYBOARD_MARKUP
    )

    # Raise ZeroDivisionError
    1/0


def main():
    updater = Updater(
        config.TOKEN,
        defaults=Defaults(run_async=True),
    )

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', on_request))
    dp.add_handler(MessageHandler(Filters.text(COMMANDS), on_reply_command))
    dp.add_handler(MessageHandler(Filters.text, on_request))

    # Handle all errors
    dp.add_error_handler(lambda update, context: reply_error(log, update, context))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
