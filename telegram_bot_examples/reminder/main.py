#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT
import time
import sys

from logging import Logger
from threading import Thread

# pip install python-telegram-bot
from telegram import Update, Bot
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackContext

sys.path.append('..')

from common import get_logger, log_func, start_bot, run_main
from db import Reminder, User, Chat
from utils import parse_command, get_pretty_datetime


def do_checking_reminders(log: Logger, bot: Bot):
    while True:
        try:
            expected_time = DT.datetime.now() - DT.timedelta(seconds=1)
            query = (
                Reminder
                .select()
                .where(
                    (Reminder.is_sent == False)
                    & (Reminder.finish_time <= expected_time)
                )
                .order_by(Reminder.finish_time)
            )

            for reminder in query:
                log.info('Send reminder: %s', reminder)

                bot.send_message(
                    chat_id=reminder.chat_id, text='⌛',
                    reply_to_message_id=reminder.message_id
                )

                reminder.is_sent = True
                reminder.save()

        except:
            log.exception('')

        finally:
            time.sleep(1)


log = get_logger(__file__)


@log_func(log)
def on_start(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        'Введите что-нибудь, например: "напомни через 1 час".\n'
        'Для получения списка напоминаний, напишите: "список"'
    )


@log_func(log)
def on_request(update: Update, context: CallbackContext):
    message = update.effective_message

    command = message.text
    log.debug(f'Command: {command!r}')

    finish_time = parse_command(command)
    if not finish_time:
        message.reply_text('Не получилось разобрать команду!')
        return

    Reminder.create(
        message_id=message.message_id,
        command=command,
        finish_time=finish_time,
        user=User.get_from(update.effective_user),
        chat=Chat.get_from(update.effective_chat),
    )

    message.reply_text(f'Напоминание установлено на {get_pretty_datetime(finish_time)}')


@log_func(log)
def on_get_reminders(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    query = (
        Reminder
        .select()
        .where(
            (Reminder.chat_id == chat.id)
            & (Reminder.user_id == user.id)
            & (Reminder.is_sent == False)
        )
        .order_by(Reminder.finish_time)
    )

    number = query.count()

    if number:
        text = f'Напоминаний ({number}):\n'
        for x in query:
            text += '    ' + get_pretty_datetime(x.finish_time) + '\n'
    else:
        text = 'Напоминаний нет'

    message.reply_text(text)


def main():
    handlers = [
        CommandHandler('start', on_start),
        MessageHandler(Filters.regex('(?i)^список$'), on_get_reminders),
        MessageHandler(Filters.text, on_request),
    ]

    def before_start_func(updater: Updater):
        # TODO: When the bot crashes, it is possible to create duplicate thread
        #       Need using global variable for getting bot
        thread = Thread(target=do_checking_reminders, args=[log, updater.bot])
        thread.start()

    start_bot(log, handlers, before_start_func)


if __name__ == '__main__':
    run_main(main, log)
