#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://core.telegram.org/bots/api#getuserprofilephotos
# SOURCE: https://python-telegram-bot.readthedocs.io/en/stable/telegram.bot.html?highlight=getUserProfilePhotos#telegram.Bot.get_user_profile_photos


# pip install python-telegram-bot
from telegram import Update
from telegram.ext import MessageHandler, CommandHandler, Filters, CallbackContext

from common import get_logger, log_func, start_bot, run_main


log = get_logger(__file__)


@log_func(log)
def on_start(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        'Write something'
    )


@log_func(log)
def on_request(update: Update, context: CallbackContext):
    message = update.effective_message
    user_id = update.effective_user.id

    result = context.bot.get_user_profile_photos(user_id)

    photos = result['photos']
    if not photos:
        message.reply_text('No profile photos!')
        return

    for photo_sizes in photos:
        photo = max(photo_sizes, key=lambda x: x['width'])
        file_id = photo['file_id']
        message.reply_photo(file_id, caption=file_id)


def main():
    handlers = [
        CommandHandler('start', on_start),
        MessageHandler(Filters.text, on_request),
    ]
    start_bot(log, handlers)


if __name__ == '__main__':
    run_main(main, log)
