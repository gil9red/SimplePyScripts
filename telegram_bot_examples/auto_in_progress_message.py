#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import functools

# pip install python-telegram-bot
import time

from telegram import Update, ReplyMarkup, Message, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackContext

from common import get_logger, log_func, start_bot, run_main


# SOURCE: https://github.com/gil9red/total_time_playlist_youtube_telegram_bot/blob/2bed7e473b73cac984e62b5ba8a47923a8a8c0ba/bot/common.py#L123
class show_temp_message:
    def __init__(
            self,
            text: str,
            update: Update,
            context: CallbackContext,
            reply_markup: ReplyMarkup = None,
            quote: bool = True,
            **kwargs,
    ):
        self.text = text
        self.update = update
        self.context = context
        self.reply_markup = reply_markup
        self.quote = quote
        self.kwargs: dict = kwargs
        self.message: Message = None

    def __enter__(self):
        self.message = self.update.effective_message.reply_text(
            text=self.text,
            reply_markup=self.reply_markup,
            quote=self.quote,
            **self.kwargs,
        )
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.message:
            self.message.delete()
        return True


def show_temp_message_decorator(
        text: str = 'In progress...',
        reply_markup: ReplyMarkup = None,
        **kwargs,
):
    def actual_decorator(func):
        @functools.wraps(func)
        def wrapper(update: Update, context: CallbackContext):
            with show_temp_message(
                text=text,
                update=update,
                context=context,
                reply_markup=reply_markup,
                **kwargs,
            ):
                return func(update, context)

        return wrapper
    return actual_decorator


log = get_logger(__file__)

ALL_COMMANDS = []


def run_command(message: Message):
    time.sleep(5)
    message.reply_text('Hello World!')


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
def on_simple(update: Update, context: CallbackContext):
    message = update.effective_message
    run_command(message)


@log_func(log)
@show_temp_message_decorator()
def on_in_progress(update: Update, context: CallbackContext):
    message = update.effective_message
    run_command(message)


@log_func(log)
@show_temp_message_decorator(text='Пожалуйста, подождите...')
def on_custom_in_progress(update: Update, context: CallbackContext):
    message = update.effective_message
    run_command(message)


@log_func(log)
@show_temp_message_decorator(
    text='<b>Пожалуйста</b>, подождите... 😊',
    parse_mode=ParseMode.HTML,
    quote=True,
    reply_markup=InlineKeyboardMarkup.from_button(
        InlineKeyboardButton(
            text='Посмотреть другие примеры',
            url='https://github.com/gil9red/SimplePyScripts/tree/815f366f8a7813cbdfdd2214241bab93b2914c10/telegram_bot_examples',
        )
    )
)
def on_custom_all_in_progress(update: Update, context: CallbackContext):
    message = update.effective_message
    run_command(message)


def main():
    handlers = [
        CommandHandler('start', on_start),
        CommandHandler('simple', on_simple),
        CommandHandler('in_progress', on_in_progress),
        CommandHandler('custom_in_progress', on_custom_in_progress),
        CommandHandler('custom_all_in_progress', on_custom_all_in_progress),
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
