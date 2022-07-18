#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
import random
import sys
from pathlib import Path
from typing import Optional

import requests

# pip install python-telegram-bot
from telegram import Update
from telegram.ext import MessageHandler, CommandHandler, Filters, CallbackContext


DIR = Path(__file__).resolve().parent

sys.path.append(str(DIR.parent))
from common import get_logger, log_func, start_bot, run_main


TOKEN_GIPHY_FILE_NAME = DIR / 'TOKEN_GIPHY.txt'

# SOURCE: https://developers.giphy.com/dashboard/
GIPHY_API_KEY = os.environ.get('TOKEN_GIPHY') or TOKEN_GIPHY_FILE_NAME.read_text('utf-8').strip()

URL_API = f'https://api.giphy.com/v1/gifs/search?api_key={GIPHY_API_KEY}'


def get_random_gif_url(query: str) -> Optional[str]:
    rs = requests.get(URL_API, params=dict(q=query))
    rs.raise_for_status()

    data = rs.json()['data']
    if not data:
        return

    return random.choice(data)['images']['original']['url']


log = get_logger(__file__)


@log_func(log)
def on_start(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        'Write something'
    )


@log_func(log)
def on_request(update: Update, context: CallbackContext):
    message = update.effective_message

    url = get_random_gif_url(message.text)
    if url:
        message.reply_document(document=url, quote=True)
    else:
        message.reply_text(text='Not found!', quote=True)


def main():
    handlers = [
        CommandHandler('start', on_start),
        MessageHandler(Filters.text, on_request),
    ]
    start_bot(log, handlers)


if __name__ == '__main__':
    run_main(main, log)
