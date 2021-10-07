#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import threading

# pip install python-telegram-bot
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, Defaults

import config


def on_request(update: Update, context: CallbackContext):
    message = update.effective_message

    message.reply_text(
        f'Thread: {threading.current_thread()}'
    )


def main():
    updater = Updater(
        config.TOKEN,
        defaults=Defaults(run_async=True),
    )

    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text, on_request))

    # NOTE: Bad:
    # dp.add_handler(MessageHandler(Filters.text, on_request, run_async=True))

    # NOTE: Better than using run_async=True parameter, but bad:
    # for commands in dp.handlers.values():
    #     for command in commands:
    #         command.run_async = True

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
