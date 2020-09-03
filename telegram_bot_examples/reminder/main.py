#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT
from logging import Logger
import os
from threading import Thread
import time
import sys
import re

# pip install python-telegram-bot
from telegram import Update, Bot
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackContext
from telegram.ext.dispatcher import run_async

sys.path.append('..')

import config
from common import get_logger, log_func, reply_error
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


@run_async
@log_func(log)
def on_start(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Введите что-нибудь, например: "напомни через 1 час".\n'
        'Для получения списка напоминаний, напишите: "список"'
    )


@run_async
@log_func(log)
def on_request(update: Update, context: CallbackContext):
    message = update.message

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


@run_async
@log_func(log)
def on_get_reminders(update: Update, context: CallbackContext):
    message = update.message
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

    # TODO: When the bot crashes, it is possible to create duplicate thread
    thread = Thread(target=do_checking_reminders, args=[log, updater.bot])
    thread.start()

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', on_start))
    dp.add_handler(MessageHandler(Filters.regex('(?i)^список$'), on_get_reminders))
    dp.add_handler(MessageHandler(Filters.text, on_request))

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
