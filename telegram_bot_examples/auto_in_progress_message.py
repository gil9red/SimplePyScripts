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
    SPINNER = '◜', '◝', '◞', '◟'
    POINTS = '.', '..', '...'
    MOON_PHASES = '🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘'
    BLOCKS = '█▒▒▒▒', '██▒▒▒', '███▒▒', '████▒', '█████'
    RECTS_LARGE = '■▢▢▢▢', '■■▢▢▢', '■■■▢▢', '■■■■▢', '■■■■■'
    RECTS_SMALL = '■□□□□', '■■□□□', '■■■□□', '■■■■□', '■■■■■'
    PARALLELOGRAMS = '▰▱▱▱▱', '▰▰▱▱▱', '▰▰▰▱▱', '▰▰▰▰▱', '▰▰▰▰▰'
    CIRCLES = '⚫⚪⚪⚪⚪', '⚫⚫⚪⚪⚪', '⚫⚫⚫⚪⚪', '⚫⚫⚫⚫⚪', '⚫⚫⚫⚫⚫'

    @classmethod
    def get_text(cls, value: str, text_fmt: str = 'In progress {value}') -> str:
        return text_fmt.format(value=value)

    def get_init_text(self, text_fmt: str = 'In progress {value}') -> str:
        return self.get_text(
            value=self.value[0],
            text_fmt=text_fmt
        )


class InfinityProgressIndicatorThread(threading.Thread):
    def __init__(
            self,
            text_fmt: str,
            message: Message,
            progress_value: ProgressValue = ProgressValue.POINTS,
            parse_mode: ParseMode = None,
            reply_markup: ReplyMarkup = None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.daemon = True

        self._stop = threading.Event()
        self._progress_bar = cycle(progress_value.value)

        self.text_fmt = text_fmt
        self.message = message
        self.parse_mode = parse_mode
        self.reply_markup = reply_markup

    def run(self):
        while not self.is_stopped():
            text = ProgressValue.get_text(
                value=next(self._progress_bar),
                text_fmt=self.text_fmt,
            )

            try:
                self.message.edit_text(
                    text=text,
                    parse_mode=self.parse_mode,
                    reply_markup=self.reply_markup,
                )
            except BadRequest:
                pass

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
            parse_mode: ParseMode = None,
            reply_markup: ReplyMarkup = None,
            quote: bool = True,
            progress_value: ProgressValue = None,
            **kwargs,
    ):
        self.text = text
        self.update = update
        self.context = context
        self.parse_mode = parse_mode
        self.reply_markup = reply_markup
        self.quote = quote
        self.kwargs: dict = kwargs
        self.message: Message = None

        self.progress_value = progress_value
        self.thread_progress: InfinityProgressIndicatorThread = None

    def __enter__(self):
        text = self.text
        if self.progress_value:
            text = self.progress_value.get_init_text(self.text)

        self.message = self.update.effective_message.reply_text(
            text=text,
            parse_mode=self.parse_mode,
            reply_markup=self.reply_markup,
            quote=self.quote,
            **self.kwargs,
        )

        if self.progress_value:
            self.thread_progress = InfinityProgressIndicatorThread(
                text_fmt=self.text,
                message=self.message,
                progress_value=self.progress_value,
                parse_mode=self.parse_mode,
                reply_markup=self.reply_markup,
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
        parse_mode: ParseMode = None,
        reply_markup: ReplyMarkup = None,
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
    text='Выполняется работа {value}',
    progress_value=ProgressValue.LINES,
)
def on_animation_lines(update: Update, context: CallbackContext):
    message = update.effective_message
    run_command(message)


@log_func(log)
@show_temp_message_decorator(
    text='Выполняется работа {value}',
    progress_value=ProgressValue.SPINNER,
)
def on_animation_spinner(update: Update, context: CallbackContext):
    message = update.effective_message
    run_command(message)


@log_func(log)
@show_temp_message_decorator(
    text='Please, wait {value}',
    progress_value=ProgressValue.POINTS,
)
def on_animation_points(update: Update, context: CallbackContext):
    message = update.effective_message
    run_command(message)


@log_func(log)
@show_temp_message_decorator(
    text='Всё зависит от <b>лунных</b> циклов {value} 😊',
    parse_mode=ParseMode.HTML,
    progress_value=ProgressValue.MOON_PHASES,
)
def on_animation_moon_phases(update: Update, context: CallbackContext):
    message = update.effective_message
    run_command(message)


@log_func(log)
@show_temp_message_decorator(
    text='Loading {value}',
    progress_value=ProgressValue.BLOCKS,
)
def on_animation_blocks(update: Update, context: CallbackContext):
    message = update.effective_message
    run_command(message)


@log_func(log)
@show_temp_message_decorator(
    text='Loading {value}',
    progress_value=ProgressValue.RECTS_LARGE,
)
def on_animation_rects_large(update: Update, context: CallbackContext):
    message = update.effective_message
    run_command(message)


@log_func(log)
@show_temp_message_decorator(
    text='Loading {value}',
    progress_value=ProgressValue.RECTS_SMALL,
)
def on_animation_rects_small(update: Update, context: CallbackContext):
    message = update.effective_message
    run_command(message)


@log_func(log)
@show_temp_message_decorator(
    text='Loading {value}',
    progress_value=ProgressValue.PARALLELOGRAMS,
)
def on_animation_parallelograms(update: Update, context: CallbackContext):
    message = update.effective_message
    run_command(message)


@log_func(log)
@show_temp_message_decorator(
    text='Loading {value}',
    progress_value=ProgressValue.CIRCLES,
)
def on_animation_circles(update: Update, context: CallbackContext):
    message = update.effective_message
    run_command(message)


@log_func(log)
@show_temp_message_decorator(
    text='{value}\n<b>Пожалуйста</b>, подождите...\n{value}\n😊',
    progress_value=ProgressValue.RECTS_SMALL,
    parse_mode=ParseMode.HTML,
    quote=False,
    reply_markup=InlineKeyboardMarkup.from_button(
        InlineKeyboardButton(
            text='Посмотреть другие примеры',
            url='https://github.com/gil9red/SimplePyScripts/tree/815f366f8a7813cbdfdd2214241bab93b2914c10/telegram_bot_examples',
        )
    )
)
def on_custom_all_animation(update: Update, context: CallbackContext):
    message = update.effective_message
    run_command(message)


def main():
    handlers = [
        CommandHandler('start', on_start),

        CommandHandler('simple', on_simple),

        CommandHandler('in_progress', on_in_progress),
        CommandHandler('custom_in_progress', on_custom_in_progress),
        CommandHandler('custom_all_in_progress', on_custom_all_in_progress),

        CommandHandler('animation_lines', on_animation_lines),
        CommandHandler('animation_spinner', on_animation_spinner),
        CommandHandler('animation_points', on_animation_points),
        CommandHandler('animation_moon_phases', on_animation_moon_phases),
        CommandHandler('animation_blocks', on_animation_blocks),
        CommandHandler('animation_rects_large', on_animation_rects_large),
        CommandHandler('animation_rects_small', on_animation_rects_small),
        CommandHandler('animation_parallelograms', on_animation_parallelograms),
        CommandHandler('animation_circles', on_animation_circles),
        CommandHandler('custom_all_animation', on_custom_all_animation),

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
