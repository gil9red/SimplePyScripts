#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
import time

# pip install python-telegram-bot
from telegram import Update
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackContext
from telegram.ext.dispatcher import run_async

import config
from common import get_logger, log_func, reply_error


log = get_logger(__file__)

ALL_COMMANDS = []


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

    text = 'Commands:\n' + '\n'.join(f'    /{x}' for x in ALL_COMMANDS)
    message.reply_text(text)


@run_async
@log_func(log)
def on_say_hello(update: Update, context: CallbackContext):
    message = update.message
    args = context.args

    if args:
        text = f'Hello, {" ".join(args)}!'
    else:
        text = 'Input name, example: /say_hello Vasya'

    message.reply_text(text)


@run_async
@log_func(log)
def on_say_hello_world(update: Update, context: CallbackContext):
    message = update.message
    message.reply_text('Hello World!')


@run_async
@log_func(log)
def on_cmd(update: Update, context: CallbackContext):
    message = update.message
    message.reply_text(f'Args: {context.args}')


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
    dp.add_handler(CommandHandler('say_hello', on_say_hello))
    dp.add_handler(CommandHandler('say_hello_world', on_say_hello_world))
    dp.add_handler(CommandHandler('cmd', on_cmd))
    dp.add_handler(MessageHandler(Filters.text, on_request))

    for commands in dp.handlers.values():
        for command in commands:
            if isinstance(command, CommandHandler):
                ALL_COMMANDS.extend(command.command)

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
