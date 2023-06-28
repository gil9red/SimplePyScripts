#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install python-telegram-bot
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    MessageHandler,
    CommandHandler,
    Filters,
    CallbackContext,
    ConversationHandler,
)

from common import get_logger, log_func, start_bot, run_main


BUTTON_START_ANKETA = "Заполнить анкету"
REPLY_KEYBOARD_MARKUP = ReplyKeyboardMarkup(
    [[BUTTON_START_ANKETA]], resize_keyboard=True
)
REPLY_KEYBOARD_MARKUP_SET_RATING = ReplyKeyboardMarkup(
    [["1", "2", "3", "4", "5"]], resize_keyboard=True, one_time_keyboard=True
)

STATE_USER_NAME = "user_name"
STATE_USER_AGE = "user_age"
STATE_RATING = "rating"
STATE_COMMENT = "comment"

ANKETA_TEXT_FORMAT = """\
Результат опроса:
    <b>Имя:</b> {name}
    <b>Возраст:</b> {age}
    <b>Оценка:</b> {rating}
    <b>Комментарий:</b> {comment}
"""


log = get_logger(__file__)


@log_func(log)
def on_start(update: Update, _: CallbackContext):
    update.effective_message.reply_text(
        "Введите что-нибудь", reply_markup=REPLY_KEYBOARD_MARKUP
    )


@log_func(log)
def on_anketa_start(update: Update, context: CallbackContext):
    context.user_data["name"] = ""
    context.user_data["age"] = ""
    context.user_data["rating"] = ""
    context.user_data["comment"] = ""

    update.effective_message.reply_text(
        "Как вас зовут?", reply_markup=ReplyKeyboardRemove()
    )
    return STATE_USER_NAME


@log_func(log)
def on_anketa_set_name(update: Update, context: CallbackContext):
    context.user_data["name"] = update.effective_message.text

    update.effective_message.reply_text("Сколько вам лет?")
    return STATE_USER_AGE


@log_func(log)
def on_anketa_set_age(update: Update, context: CallbackContext):
    message = update.effective_message
    context.user_data["age"] = message.text

    message.reply_text(
        "Оцените статью от 1 до 5", reply_markup=REPLY_KEYBOARD_MARKUP_SET_RATING
    )
    return STATE_RATING


@log_func(log)
def on_anketa_set_rating(update: Update, context: CallbackContext):
    message = update.effective_message
    context.user_data["rating"] = message.text

    message.reply_text(
        "Напишите отзыв или нажмите кнопку пропустить этот шаг.",
        reply_markup=ReplyKeyboardMarkup(
            [["Пропустить"]], resize_keyboard=True, one_time_keyboard=True
        ),
    )
    return STATE_COMMENT


@log_func(log)
def on_anketa_comment(update: Update, context: CallbackContext):
    message = update.effective_message
    context.user_data["comment"] = message.text
    text = ANKETA_TEXT_FORMAT.format(**context.user_data)

    message.reply_html(text)
    message.reply_text(
        "Спасибо вам за комментарий!", reply_markup=REPLY_KEYBOARD_MARKUP
    )

    return ConversationHandler.END


@log_func(log)
def on_anketa_exit_comment(update: Update, context: CallbackContext):
    message = update.effective_message
    text = ANKETA_TEXT_FORMAT.format(**context.user_data)

    message.reply_html(text)
    message.reply_text("Спасибо!", reply_markup=REPLY_KEYBOARD_MARKUP)

    return ConversationHandler.END  # выходим из диалог


@log_func(log)
def on_anketa_invalid_set_rating(update: Update, _: CallbackContext):
    update.effective_message.reply_text(
        "Я вас не понимаю, выберите оценку на клавиатуре!",
        reply_markup=REPLY_KEYBOARD_MARKUP_SET_RATING,
    )


@log_func(log)
def on_request(update: Update, _: CallbackContext):
    message = update.effective_message

    message.reply_text("Echo: " + message.text, reply_markup=REPLY_KEYBOARD_MARKUP)


def main():
    handlers = [
        CommandHandler("start", on_start),
        ConversationHandler(
            entry_points=[
                MessageHandler(Filters.regex(BUTTON_START_ANKETA), on_anketa_start)
            ],
            states={
                STATE_USER_NAME: [MessageHandler(Filters.text, on_anketa_set_name)],
                STATE_USER_AGE: [MessageHandler(Filters.text, on_anketa_set_age)],
                STATE_RATING: [
                    MessageHandler(Filters.regex("1|2|3|4|5"), on_anketa_set_rating)
                ],
                STATE_COMMENT: [
                    MessageHandler(Filters.regex("Пропустить"), on_anketa_exit_comment),
                    MessageHandler(Filters.text, on_anketa_comment),
                ],
            },
            fallbacks=[
                MessageHandler(
                    Filters.text | Filters.video | Filters.photo | Filters.document,
                    on_anketa_invalid_set_rating,
                )
            ],
        ),
        MessageHandler(Filters.text, on_request),
    ]
    start_bot(log, handlers)


if __name__ == "__main__":
    run_main(main, log)
