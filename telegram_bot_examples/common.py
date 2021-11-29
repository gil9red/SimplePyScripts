#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import functools
import logging
import os
import sys
import re
import time

from pathlib import Path
from typing import Callable, List

from telegram import Update
from telegram.ext import Updater, CallbackContext, Handler, Defaults

import config


def get_logger(file_name: str, dir_name='logs'):
    dir_name = Path(dir_name).resolve()
    dir_name.mkdir(parents=True, exist_ok=True)

    file_name = str(dir_name / Path(file_name).resolve().name) + '.log'

    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] %(filename)s[LINE:%(lineno)d] %(levelname)-8s %(message)s')

    fh = logging.FileHandler(file_name, encoding='utf-8')
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(logging.DEBUG)

    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    log.addHandler(fh)
    log.addHandler(ch)

    return log


def log_func(log: logging.Logger):
    def actual_decorator(func):
        @functools.wraps(func)
        def wrapper(update: Update, context: CallbackContext):
            if update:
                chat_id = user_id = first_name = last_name = username = language_code = None

                if update.effective_chat:
                    chat_id = update.effective_chat.id

                if update.effective_user:
                    user_id = update.effective_user.id
                    first_name = update.effective_user.first_name
                    last_name = update.effective_user.last_name
                    username = update.effective_user.username
                    language_code = update.effective_user.language_code

                try:
                    message = update.effective_message.text
                except:
                    message = ''

                try:
                    query_data = update.callback_query.data
                except:
                    query_data = ''

                msg = f'[chat_id={chat_id}, user_id={user_id}, ' \
                      f'first_name={first_name!r}, last_name={last_name!r}, ' \
                      f'username={username!r}, language_code={language_code}, ' \
                      f'message={message!r}, query_data={query_data!r}]'
                msg = func.__name__ + msg

                log.debug(msg)

            return func(update, context)

        return wrapper
    return actual_decorator


def reply_error(log: logging.Logger, update: Update, context: CallbackContext):
    log.error('Error: %s\nUpdate: %s', context.error, update, exc_info=context.error)
    if update:
        update.effective_message.reply_text(config.ERROR_TEXT)


def fill_string_pattern(pattern: re.Pattern, *args) -> str:
    pattern = pattern.pattern
    pattern = pattern.strip('^$')
    return re.sub(r'\(.+?\)', '{}', pattern).format(*args)


def start_bot(
        log: logging.Logger,
        handlers: List[Handler],
        before_start_func: Callable[[Updater], None] = None,
        **updater_kwargs,
):
    log.debug('Start')

    cpu_count = os.cpu_count()
    workers = cpu_count
    log.debug(f'System: CPU_COUNT={cpu_count}, WORKERS={workers}')

    # Create the EventHandler and pass it your bot's token.
    updater = Updater(
        config.TOKEN,
        workers=workers,
        defaults=Defaults(run_async=True),
        **updater_kwargs,
    )
    bot_info = updater.bot.get_me()
    log.debug(f'Bot name: {bot_info.first_name!r} (@{bot_info.username})')

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    for handler in handlers:
        dp.add_handler(handler)

    # Handle all errors
    dp.add_error_handler(lambda update, context: reply_error(log, update, context))

    if before_start_func:
        before_start_func(updater)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

    log.debug('Finish')


def run_main(main_func: Callable, log: logging.Logger, timeout=15):
    while True:
        try:
            main_func()
        except:
            log.exception('')

            log.info(f'Restarting the bot after {timeout} seconds')
            time.sleep(timeout)
