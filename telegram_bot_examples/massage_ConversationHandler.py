#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://ru.stackoverflow.com/q/1174642/201445
# SOURCE: https://ru.stackoverflow.com/q/1175226/201445


import sys

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from telegram.ext import (
    Updater,
    MessageHandler,
    CommandHandler,
    Filters,
    CallbackContext,
    CallbackQueryHandler,
    ConversationHandler,
    Defaults,
)

from config import TOKEN
from common import get_logger, log_func

sys.path.append("calendar_example")
import telegramcalendar


log = get_logger(__file__)


# TODO: enum
STATE_SELECT_MASSAGE = "STATE_SELECT_MASSAGE"
STATE_SELECT_DATE = "STATE_SELECT_DATE"
STATE_SELECT_TIME = "STATE_SELECT_TIME"
STATE_SELECT_USER = "STATE_SELECT_USER"
STATE_SELECT_PHONE = "STATE_SELECT_PHONE"
STATE_FINISH = "STATE_FINISH"


def facts_to_str(user_data: dict) -> str:
    facts = []
    for key, value in user_data.items():
        facts.append(f"{key} - {value}")
    return "\n".join(facts).join(["\n", "\n"])


@log_func(log)
def on_main_menu(update: Update, _: CallbackContext) -> None:
    # Если функция вызвана из CallbackQueryHandler
    query = update.callback_query
    if query:
        query.answer()

    message = update.effective_message
    user_id = update.effective_user.id
    print(f"User ID: {user_id} ")

    keyboard = [
        [
            InlineKeyboardButton("О мастере 🧑🏻", callback_data="master"),
            InlineKeyboardButton("Контакты ☎️", callback_data="contacts"),
            InlineKeyboardButton("Виды массажа", callback_data="types_massage"),
        ],
        [
            InlineKeyboardButton("Записаться‍", callback_data="sing_up"),
            InlineKeyboardButton("Отменить запись", callback_data="cancel"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = """Здравствуйте! 
Я личный помощник Вашего мастера.
C моей помощью Вы можете узнать о видах массажа, записаться на сеанс или отменить свою запись.
С чего начнём? ⬇️"""

    if query:
        message.edit_text(text, reply_markup=reply_markup)
    else:
        message.reply_text(text, reply_markup=reply_markup)


@log_func(log)
def on_sing_up(update: Update, _: CallbackContext):
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Классический", callback_data="klass"),
            InlineKeyboardButton("Лечебный", callback_data="lech"),
            InlineKeyboardButton("Медовый", callback_data="med"),
        ],
        [
            InlineKeyboardButton("Лимфодренажный", callback_data="limfo"),
            InlineKeyboardButton("Антицеллюлитный", callback_data="anti"),
        ],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(text="Выберите вид массажа: ⬇️", reply_markup=reply_markup)

    return STATE_SELECT_MASSAGE


@log_func(log)
def on_massage_klassik(update: Update, context: CallbackContext):
    user_data = context.user_data
    category = "Вид массажа"
    massage = "Классический"
    user_data[category] = massage

    query = update.callback_query
    query.answer()

    query.edit_message_text(
        "Выберите дату: ", reply_markup=telegramcalendar.create_calendar()
    )

    return STATE_SELECT_DATE


@log_func(log)
def on_massage_lechebny(update: Update, context: CallbackContext):
    user_data = context.user_data
    category = "Вид массажа"
    massage = "Лечебный"
    user_data[category] = massage

    query = update.callback_query
    query.answer()

    query.edit_message_text(
        "Выберите дату: ", reply_markup=telegramcalendar.create_calendar()
    )

    return STATE_SELECT_DATE


@log_func(log)
def on_massage_medovy(update: Update, context: CallbackContext):
    user_data = context.user_data
    category = "Вид массажа"
    massage = "Медовый"
    user_data[category] = massage

    query = update.callback_query
    query.answer()

    query.edit_message_text(
        "Выберите дату: ", reply_markup=telegramcalendar.create_calendar()
    )

    return STATE_SELECT_DATE


@log_func(log)
def on_massage_limfo(update: Update, context: CallbackContext):
    user_data = context.user_data
    category = "Вид массажа"
    massage = "Лимфодренажный"
    user_data[category] = massage

    query = update.callback_query
    query.answer()

    query.edit_message_text(
        "Выберите дату: ", reply_markup=telegramcalendar.create_calendar()
    )

    return STATE_SELECT_DATE


@log_func(log)
def on_massage_anti(update: Update, context: CallbackContext):
    user_data = context.user_data
    category = "Вид массажа"
    massage = "Антицеллюлитный"
    user_data[category] = massage

    query = update.callback_query
    query.answer()

    query.edit_message_text(
        "Выберите дату: ", reply_markup=telegramcalendar.create_calendar()
    )

    return STATE_SELECT_DATE


@log_func(log)
def on_select_date(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    bot = context.bot

    selected, date = telegramcalendar.process_calendar_selection(bot, update)
    if selected:
        user_data = context.user_data
        text = date.strftime("%d/%m/%Y")
        user_data["Дата"] = text

        keyboard = [
            [
                InlineKeyboardButton("12:00", callback_data="12"),
                InlineKeyboardButton("14:30", callback_data="14"),
                InlineKeyboardButton("16:00", callback_data="16"),
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        query.message.reply_text(
            text="""Вы выбрали %s
Выберите свободное время: """
            % text,
            reply_markup=reply_markup,
        )

        return STATE_SELECT_TIME


@log_func(log)
def on_time_12(update: Update, context: CallbackContext):
    user_data = context.user_data

    text = "12:00"
    user_data["Время"] = text

    query = update.callback_query
    query.answer()

    query.edit_message_text("""Введите своё *Имя и Фамилию*""", parse_mode="Markdown")

    return STATE_SELECT_USER


@log_func(log)
def on_time_14(update: Update, context: CallbackContext):
    user_data = context.user_data

    text = "14:30"
    user_data["Время"] = text

    query = update.callback_query
    query.answer()

    query.edit_message_text("""Введите своё *Имя и Фамилию*""", parse_mode="Markdown")

    return STATE_SELECT_USER


@log_func(log)
def on_time_16(update: Update, context: CallbackContext):
    user_data = context.user_data

    text = "16:00"
    user_data["Время"] = text

    query = update.callback_query
    query.answer()

    query.edit_message_text("""Введите своё *Имя и Фамилию*""", parse_mode="Markdown")

    return STATE_SELECT_USER


@log_func(log)
def on_sing_name(update: Update, context: CallbackContext):
    user_data = context.user_data
    category = "Имя Фамилия"
    user_name = update.effective_message.text
    user_data[category] = user_name
    print("Сохранено имя: " + user_name)

    contact_keyboard = KeyboardButton("Отправить номер", request_contact=True)
    custom_keyboard = [[contact_keyboard]]
    markup = ReplyKeyboardMarkup(
        custom_keyboard, resize_keyboard=True, one_time_keyboard=True
    )

    update.effective_message.reply_text(
        """*Введите свой номер телефона*""", parse_mode="Markdown", reply_markup=markup
    )

    return STATE_SELECT_PHONE


@log_func(log)
def on_sing_contact(update: Update, context: CallbackContext):
    message = update.effective_message
    user_data = context.user_data
    category = "Телефон"
    phone = message.text or message.contact.phone_number
    user_data[category] = phone
    print("Сохранен номер: " + phone)

    keyboard = [
        [
            InlineKeyboardButton("Подтвердить", callback_data="okay"),
            InlineKeyboardButton("Изменить запись", callback_data="recording"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    message.reply_text(
        f"""
*Вы зарегистрированы!*

_Ваши данные:_ 
{facts_to_str(user_data)}
        """,
        parse_mode="Markdown",
        reply_markup=reply_markup,
    )

    return STATE_FINISH


@log_func(log)
def on_finish(update: Update, _: CallbackContext):
    query = update.callback_query
    query.answer()

    query.edit_message_text(
        """*Спасибо за регистрацию!*

Мастер будет ожидать Вас.""",
        parse_mode="Markdown",
    )

    return ConversationHandler.END


@log_func(log)
def on_recording(update: Update, context: CallbackContext):
    return on_sing_up(update, context)


def on_error(update, context) -> None:
    """Log Errors caused by Updates."""
    log.warning('Update "%s" caused error "%s"', update, context.error)


def main() -> None:
    updater = Updater(
        token=TOKEN,
        defaults=Defaults(run_async=True),
    )

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", on_main_menu))

    dp.add_handler(
        ConversationHandler(
            entry_points=[
                CommandHandler("start", on_main_menu),
                CallbackQueryHandler(on_sing_up, pattern="sing_up"),
            ],
            states={
                STATE_SELECT_MASSAGE: [
                    CallbackQueryHandler(on_massage_klassik, pattern="klass"),
                    CallbackQueryHandler(on_massage_lechebny, pattern="lech"),
                    CallbackQueryHandler(on_massage_medovy, pattern="med"),
                    CallbackQueryHandler(on_massage_limfo, pattern="limfo"),
                    CallbackQueryHandler(on_massage_anti, pattern="anti"),
                    CallbackQueryHandler(on_main_menu, pattern="main_menu"),
                ],
                STATE_SELECT_DATE: [CallbackQueryHandler(on_select_date)],
                STATE_SELECT_TIME: [
                    CallbackQueryHandler(on_time_12, pattern="12"),
                    CallbackQueryHandler(on_time_14, pattern="14"),
                    CallbackQueryHandler(on_time_16, pattern="16"),
                ],
                STATE_SELECT_USER: [MessageHandler(Filters.text, on_sing_name)],
                STATE_SELECT_PHONE: [
                    MessageHandler(Filters.text | Filters.contact, on_sing_contact)
                ],
                STATE_FINISH: [
                    CallbackQueryHandler(on_finish, pattern="okay"),
                    CallbackQueryHandler(on_recording, pattern="recording"),
                ],
            },
            fallbacks=[],
            # allow_reentry=True,
            # per_message=True,
        )
    )

    dp.add_error_handler(on_error)

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
