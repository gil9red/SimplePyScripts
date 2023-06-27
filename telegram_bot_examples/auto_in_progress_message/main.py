#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import time

from pathlib import Path


DIR = Path(__file__).parent.resolve()
sys.path.append(str(DIR.parent))


# pip install python-telegram-bot
from telegram import (
    Update,
    Message,
    ParseMode,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    Updater,
    MessageHandler,
    CommandHandler,
    Filters,
    CallbackContext,
)

from common import get_logger, log_func, start_bot, run_main
from auto_in_progress_message.core import show_temp_message_decorator, ProgressValue


log = get_logger(__file__)

ALL_COMMANDS = []


def run_command(message: Message, sleep_seconds: int = 10):
    time.sleep(sleep_seconds)
    message.reply_text("Hello World!")


@log_func(log)
def on_start(update: Update, _: CallbackContext):
    update.effective_message.reply_text("Write something")


@log_func(log)
def on_request(update: Update, _: CallbackContext):
    message = update.effective_message

    text = "Commands:\n" + "\n".join(f"    /{x}" for x in ALL_COMMANDS)
    message.reply_text(text)


@log_func(log)
def on_simple(update: Update, _: CallbackContext):
    message = update.effective_message
    run_command(message)


@log_func(log)
@show_temp_message_decorator()
def on_in_progress(update: Update, _: CallbackContext):
    message = update.effective_message
    run_command(message)


@log_func(log)
@show_temp_message_decorator(text="Пожалуйста, подождите...")
def on_custom_in_progress(update: Update, _: CallbackContext):
    message = update.effective_message
    run_command(message)


@log_func(log)
@show_temp_message_decorator(
    text="<b>Пожалуйста</b>, подождите... 😊",
    parse_mode=ParseMode.HTML,
    quote=False,
    reply_markup=InlineKeyboardMarkup.from_button(
        InlineKeyboardButton(
            text="Посмотреть другие примеры",
            url="https://github.com/gil9red/SimplePyScripts/tree/815f366f8a7813cbdfdd2214241bab93b2914c10/telegram_bot_examples",
        )
    ),
)
def on_custom_all_in_progress(update: Update, _: CallbackContext):
    message = update.effective_message
    run_command(message)


@log_func(log)
@show_temp_message_decorator(
    text="Выполняется работа {value}",
    progress_value=ProgressValue.LINES,
)
def on_animation_lines(update: Update, _: CallbackContext):
    message = update.effective_message
    run_command(message)


@log_func(log)
@show_temp_message_decorator(
    text="Выполняется работа {value}",
    progress_value=ProgressValue.SPINNER,
)
def on_animation_spinner(update: Update, _: CallbackContext):
    message = update.effective_message
    run_command(message)


@log_func(log)
@show_temp_message_decorator(
    text="Please, wait {value}",
    progress_value=ProgressValue.POINTS,
)
def on_animation_points(update: Update, _: CallbackContext):
    message = update.effective_message
    run_command(message)


@log_func(log)
@show_temp_message_decorator(
    text="Всё зависит от <b>лунных</b> циклов {value} 😊",
    parse_mode=ParseMode.HTML,
    progress_value=ProgressValue.MOON_PHASES_1,
)
def on_animation_moon_phases1(update: Update, _: CallbackContext):
    message = update.effective_message
    run_command(message)


@log_func(log)
@show_temp_message_decorator(
    text="Всё зависит от <b>лунных</b> циклов {value} 😊",
    parse_mode=ParseMode.HTML,
    progress_value=ProgressValue.MOON_PHASES_2,
)
def on_animation_moon_phases2(update: Update, _: CallbackContext):
    message = update.effective_message
    run_command(message)


@log_func(log)
@show_temp_message_decorator(
    text="Loading {value}",
    progress_value=ProgressValue.BLOCKS,
)
def on_animation_blocks(update: Update, _: CallbackContext):
    message = update.effective_message
    run_command(message)


@log_func(log)
@show_temp_message_decorator(
    text="Loading {value}",
    progress_value=ProgressValue.RECTS_LARGE,
)
def on_animation_rects_large(update: Update, _: CallbackContext):
    message = update.effective_message
    run_command(message)


@log_func(log)
@show_temp_message_decorator(
    text="Loading {value}",
    progress_value=ProgressValue.RECTS_SMALL,
)
def on_animation_rects_small(update: Update, _: CallbackContext):
    message = update.effective_message
    run_command(message)


@log_func(log)
@show_temp_message_decorator(
    text="Loading {value}",
    progress_value=ProgressValue.PARALLELOGRAMS,
)
def on_animation_parallelograms(update: Update, _: CallbackContext):
    message = update.effective_message
    run_command(message)


@log_func(log)
@show_temp_message_decorator(
    text="Loading {value}",
    progress_value=ProgressValue.CIRCLES,
)
def on_animation_circles(update: Update, _: CallbackContext):
    message = update.effective_message
    run_command(message)


@log_func(log)
@show_temp_message_decorator(
    text="{value}\n"
    "<b>Пожалуйста</b>, подождите...\n"
    "{value}\n"
    "Прошло {seconds} с 😊",
    progress_value=ProgressValue.RECTS_SMALL,
    parse_mode=ParseMode.HTML,
    quote=False,
    reply_markup=InlineKeyboardMarkup.from_button(
        InlineKeyboardButton(
            text="Посмотреть другие примеры",
            url="https://github.com/gil9red/SimplePyScripts/tree/815f366f8a7813cbdfdd2214241bab93b2914c10/telegram_bot_examples",
        )
    ),
)
def on_custom_all_animation(update: Update, _: CallbackContext):
    message = update.effective_message
    run_command(message)


@log_func(log)
@show_temp_message_decorator(
    text="{value} x {value}",
    progress_value=ProgressValue.RECTS_SMALL,
)
def on_custom_no_text_animation(update: Update, _: CallbackContext):
    message = update.effective_message
    run_command(message)


@log_func(log)
@show_temp_message_decorator(
    text="KFC {value}",
    progress_value=ProgressValue.CHICKENS,
)
def on_sub_animation_chickens(update: Update, _: CallbackContext):
    message = update.effective_message
    run_command(message, sleep_seconds=30)


@log_func(log)
@show_temp_message_decorator(
    text="Faces {value}",
    progress_value=ProgressValue.FACES,
)
def on_sub_animation_faces(update: Update, _: CallbackContext):
    message = update.effective_message
    run_command(message, sleep_seconds=30)


def main():
    handlers = [
        CommandHandler("start", on_start),
        CommandHandler("simple", on_simple),
        CommandHandler("in_progress", on_in_progress),
        CommandHandler("custom_in_progress", on_custom_in_progress),
        CommandHandler("custom_all_in_progress", on_custom_all_in_progress),
        CommandHandler("animation_lines", on_animation_lines),
        CommandHandler("animation_spinner", on_animation_spinner),
        CommandHandler("animation_points", on_animation_points),
        CommandHandler("animation_moon_phases1", on_animation_moon_phases1),
        CommandHandler("animation_moon_phases2", on_animation_moon_phases2),
        CommandHandler("animation_blocks", on_animation_blocks),
        CommandHandler("animation_rects_large", on_animation_rects_large),
        CommandHandler("animation_rects_small", on_animation_rects_small),
        CommandHandler("animation_parallelograms", on_animation_parallelograms),
        CommandHandler("animation_circles", on_animation_circles),
        CommandHandler("custom_all_animation", on_custom_all_animation),
        CommandHandler("custom_no_text_animation", on_custom_no_text_animation),
        CommandHandler("sub_animation_chickens", on_sub_animation_chickens),
        CommandHandler("sub_animation_faces", on_sub_animation_faces),
        MessageHandler(Filters.text, on_request),
    ]

    def before_start_func(updater: Updater):
        for commands in updater.dispatcher.handlers.values():
            for command in commands:
                if isinstance(command, CommandHandler):
                    ALL_COMMANDS.extend(command.command)

    start_bot(log, handlers, before_start_func)


if __name__ == "__main__":
    run_main(main, log)
