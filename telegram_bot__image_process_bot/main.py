#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install python-telegram-bot --upgrade
from telegram import ReplyKeyboardMarkup, ChatAction
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

from config import TOKEN, TIMEOUT, LAST_IMAGE_DIR

import requests
import os

# pip install Pillow
from PIL import Image


import functools


def get_logger(name, file='log.txt', encoding='utf-8'):
    import logging
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] %(filename)s:%(lineno)d %(levelname)-8s %(message)s')

    # Simple file handler
    # fh = logging.FileHandler(file, encoding=encoding)
    # or:
    from logging.handlers import RotatingFileHandler
    fh = RotatingFileHandler(file, maxBytes=10000000, backupCount=5, encoding=encoding)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    import sys
    sh = logging.StreamHandler(stream=sys.stdout)
    sh.setFormatter(formatter)
    log.addHandler(sh)

    return log


log = get_logger(__file__)


def log_func(func):
    @functools.wraps(func)
    def decorator(self, *args, **kwargs):
        log.debug('Entering: %s', func.__name__)
        result = func(self, *args, **kwargs)
        log.debug('Result: %s', result)
        log.debug('Exiting: %s', func.__name__)

        return result

    return decorator


from commands import invert, gray, invert_gray, pixelate, get_image_info
COMMANDS = {
    'invert': invert,
    'gray': gray,
    'invert_gray': invert_gray,
    'pixelate': pixelate,
    'get_image_info': get_image_info,
}
BUTTON_LIST = [
    sorted(COMMANDS),
]
REPLY_KEYBOARD_MARKUP = ReplyKeyboardMarkup(BUTTON_LIST, resize_keyboard=True)


if not os.path.exists(LAST_IMAGE_DIR):
    os.makedirs(LAST_IMAGE_DIR)


def get_file_name_image(user_id):
    return '{}/{}.jpg'.format(LAST_IMAGE_DIR, user_id)


# Отправка сообщения на команду /start
def start(bot, update):
    log.debug('start')

    update.message.reply_text('Отправь мне картинку')


@log_func
def work_text(bot, update):
    log.debug('work_text')

    chat_id = update.message.chat_id

    text = update.message.text
    log.debug('text: %s', text)

    if text not in COMMANDS:
        update.message.reply_text('Неизвестная команда "{}"'.format(text), timeout=TIMEOUT)
        return

    bot.send_chat_action(chat_id, action=ChatAction.UPLOAD_PHOTO)

    file_name = get_file_name_image(chat_id)

    if not os.path.exists(file_name):
        update.message.reply_text('Нужно отправить мне картинку', timeout=TIMEOUT)
        return

    img = Image.open(file_name)
    log.debug('img: %s', img)

    # Получение и вызов функции
    result = COMMANDS[text](img)

    if type(result) == str:
        log.debug('reply_text')

        update.message.reply_text(result, timeout=TIMEOUT)

    else:
        log.debug('reply_photo')

        file_name = get_file_name_image('out_{}'.format(chat_id))
        result.save(file_name, result.format)

        update.message.reply_photo(open(file_name, 'rb'), timeout=TIMEOUT)

        os.remove(file_name)


def work_photo(bot, update):
    log.debug('work_photo')

    chat_id = update.message.chat_id

    log.debug('Скачиваю картинку...')
    update.message.reply_text('Скачиваю картинку...', timeout=TIMEOUT)

    bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    url = update.message.photo[-1].get_file().file_path

    rs = requests.get(url)

    file_name = get_file_name_image(chat_id)
    with open(file_name, 'wb') as f:
        f.write(rs.content)

    log.debug('Картинка скачана!')
    update.message.reply_text('Картинка скачана!', timeout=TIMEOUT)

    update.message.reply_text(
        "Теперь ты можешь выбрать команду над последней загруженной картинкой",
        reply_markup=REPLY_KEYBOARD_MARKUP,
        timeout=TIMEOUT
    )


def error(bot, update, error):
    log.warning('Error: "%s".\nUpdate: "%s"', error, update)
    update.message.reply_text('Error: "{}"'.format(error), timeout=TIMEOUT)


if __name__ == '__main__':
    log.debug('Start')

    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text, work_text))
    dp.add_handler(MessageHandler(Filters.photo, work_photo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

    log.debug('Finish')
