#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install python-telegram-bot
from telegram import Update
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackContext

from common import get_logger, log_func, start_bot, run_main


log = get_logger(__file__)

ALL_COMMANDS = []


@log_func(log)
def on_start(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        'Write something'
    )


@log_func(log)
def on_request(update: Update, context: CallbackContext):
    message = update.effective_message

    text = 'Commands:\n' + '\n'.join(f'    /{x}' for x in ALL_COMMANDS)
    message.reply_text(text)


@log_func(log)
def on_say_hello(update: Update, context: CallbackContext):
    message = update.effective_message
    args = context.args

    if args:
        text = f'Hello, {" ".join(args)}!'
    else:
        text = 'Input name, example: /say_hello Vasya'

    message.reply_text(text)


@log_func(log)
def on_say_hello_world(update: Update, context: CallbackContext):
    message = update.effective_message
    message.reply_text('Hello World!')


@log_func(log)
def on_cmd(update: Update, context: CallbackContext):
    message = update.effective_message
    message.reply_text(f'Args: {context.args}')


def main():
    handlers = [
        CommandHandler('start', on_start),
        CommandHandler('say_hello', on_say_hello),
        CommandHandler('say_hello_world', on_say_hello_world),
        CommandHandler('cmd', on_cmd),
        MessageHandler(Filters.text, on_request),
    ]

    def before_start_func(updater: Updater):
        for commands in updater.dispatcher.handlers.values():
            for command in commands:
                if isinstance(command, CommandHandler):
                    ALL_COMMANDS.extend(command.command)

    start_bot(log, handlers, before_start_func)


if __name__ == '__main__':
    run_main(main, log)
