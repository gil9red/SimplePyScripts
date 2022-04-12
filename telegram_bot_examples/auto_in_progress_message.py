#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import enum
import functools
import threading
import time

from itertools import cycle

# pip install python-telegram-bot
from telegram import Update, ReplyMarkup, Message, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackContext
from telegram.error import BadRequest

from common import get_logger, log_func, start_bot, run_main


class ProgressValue(enum.Enum):
    LINES = '|', '/', '-', '\\'
    POINTS = '.', '..', '...'
    MOON_PHASES = '🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘'


class InfinityProgressIndicatorThread(threading.Thread):
    def __init__(
            self,
            text: str,
            message: Message,
            progress_value: ProgressValue = ProgressValue.POINTS,
            parse_mode: ParseMode = None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.daemon = True

        self._stop = threading.Event()
        self._progress_bar = cycle(progress_value.value)

        self.text = text
        self.message = message
        self.parse_mode = parse_mode

    def run(self):
        while not self.is_stopped():
            text = f'{self.text} {next(self._progress_bar)}'

            try:
                self.message.edit_text(text, parse_mode=self.parse_mode)
            except BadRequest:
                return

            time.sleep(1)

    def stop(self):
        self._stop.set()

    def is_stopped(self) -> bool:
        return self._stop.is_set()


class show_temp_message:
    def __init__(
            self,
            text: str,
            update: Update,
            context: CallbackContext,
            reply_markup: ReplyMarkup = None,
            quote: bool = True,
            parse_mode: ParseMode = None,
            progress_value: ProgressValue = None,
            **kwargs,
    ):
        self.text = text
        self.update = update
        self.context = context
        self.reply_markup = reply_markup
        self.quote = quote
        self.parse_mode = parse_mode
        self.kwargs: dict = kwargs
        self.message: Message = None

        self.progress_value = progress_value
        self.thread_progress: InfinityProgressIndicatorThread = None

    def __enter__(self):
        self.message = self.update.effective_message.reply_text(
            text=self.text,
            reply_markup=self.reply_markup,
            quote=self.quote,
            parse_mode=self.parse_mode,
            **self.kwargs,
        )

        if self.progress_value:
            self.thread_progress = InfinityProgressIndicatorThread(
                text=self.text,
                message=self.message,
                progress_value=self.progress_value,
                parse_mode=self.parse_mode,
            )
            self.thread_progress.start()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.thread_progress:
            self.thread_progress.stop()

        if self.message:
            self.message.delete()


def show_temp_message_decorator(
        text: str = 'In progress...',
        reply_markup: ReplyMarkup = None,
        parse_mode: ParseMode = None,
        progress_value: ProgressValue = None,
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
                parse_mode=parse_mode,
                progress_value=progress_value,
                **kwargs,
            ):
                return func(update, context)

        return wrapper
    return actual_decorator


log = get_logger(__file__)

ALL_COMMANDS = []


def run_command(message: Message):
    time.sleep(10)
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
    quote=False,
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


@log_func(log)
@show_temp_message_decorator(
    text='Please, wait',
    progress_value=ProgressValue.POINTS,
)
def on_in_progress_with_animation1(update: Update, context: CallbackContext):
    message = update.effective_message
    run_command(message)


@log_func(log)
@show_temp_message_decorator(
    text='Выполняется работа',
    progress_value=ProgressValue.LINES,
)
def on_in_progress_with_animation2(update: Update, context: CallbackContext):
    message = update.effective_message
    run_command(message)


@log_func(log)
@show_temp_message_decorator(
    text='Всё зависит от <b>лунных</b> циклов',
    parse_mode=ParseMode.HTML,
    progress_value=ProgressValue.MOON_PHASES,
)
def on_in_progress_with_animation3(update: Update, context: CallbackContext):
    message = update.effective_message
    run_command(message)


def main():
    handlers = [
        CommandHandler('start', on_start),
        CommandHandler('simple', on_simple),
        CommandHandler('in_progress', on_in_progress),
        CommandHandler('custom_in_progress', on_custom_in_progress),
        CommandHandler('custom_all_in_progress', on_custom_all_in_progress),
        CommandHandler('in_progress_with_animation1', on_in_progress_with_animation1),
        CommandHandler('in_progress_with_animation2', on_in_progress_with_animation2),
        CommandHandler('in_progress_with_animation3', on_in_progress_with_animation3),
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
