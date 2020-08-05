#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
import time

import requests

# pip install Pillow
from PIL import Image

# pip install python-telegram-bot --upgrade
from telegram import ReplyKeyboardMarkup, ChatAction, Update
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackContext
from telegram.ext.dispatcher import run_async

import config
from commands import invert, gray, invert_gray, pixelate, get_image_info, jackal_jpg, thumbnail, blur
from common import get_logger, log_func


log = get_logger(__file__)


COMMANDS = {
    'invert': invert,
    'gray': gray,
    'invert_gray': invert_gray,
    'get_image_info': get_image_info,
    'pixelate': pixelate,
    'pixelate16': lambda img: pixelate(img, 16),
    'pixelate32': lambda img: pixelate(img, 32),
    'pixelate48': lambda img: pixelate(img, 48),
    'jackal_jpg': jackal_jpg,
    'thumbnail32': lambda img: thumbnail(img, (32, 32)),
    'thumbnail64': lambda img: thumbnail(img, (64, 64)),
    'thumbnail128': lambda img: thumbnail(img, (128, 129)),
    'blur': blur,
    'blur5': lambda img: blur(img, 5),
    'original': lambda img: img
}
BUTTON_LIST = [
    ['invert', 'gray', 'invert_gray', 'jackal_jpg'],
    ['pixelate', 'pixelate16', 'pixelate32', 'pixelate48'],
    ['thumbnail32', 'thumbnail64', 'thumbnail128'],
    ['get_image_info', 'blur', 'blur5', 'original'],
]
REPLY_KEYBOARD_MARKUP = ReplyKeyboardMarkup(BUTTON_LIST, resize_keyboard=True)


os.makedirs(config.LAST_IMAGE_DIR, exist_ok=True)


def get_file_name_image(user_id):
    return f'{config.LAST_IMAGE_DIR}/{user_id}.jpg'


@run_async
@log_func(log)
def start(update: Update, context: CallbackContext):
    log.debug('chat: %s', update.message.chat)

    update.message.reply_text('Отправь мне картинку')


@run_async
@log_func(log)
def on_request(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text
    log.debug('text: %s', text)

    if text not in COMMANDS:
        update.message.reply_text(f'Неизвестная команда {text!r}')
        return

    context.bot.send_chat_action(chat_id, action=ChatAction.UPLOAD_PHOTO)

    file_name = get_file_name_image(chat_id)
    if not os.path.exists(file_name):
        update.message.reply_text('Нужно отправить мне картинку')
        return

    img = Image.open(file_name)
    log.debug('img: %s', img)

    # Получение и вызов функции
    result = COMMANDS[text](img)

    if type(result) == str:
        log.debug('reply_text')
        update.message.reply_text(result)
    else:
        log.debug('reply_photo')

        file_name = get_file_name_image(f'out_{chat_id}')
        result.save(file_name, result.format)

        update.message.reply_photo(open(file_name, 'rb'))

        os.remove(file_name)


@run_async
@log_func(log)
def on_photo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    log.debug('chat: %s', update.message.chat)

    msg = 'Скачиваю картинку...'
    log.debug(msg)
    progress_message = update.message.reply_text(msg + '\n⬜⬜⬜⬜⬜')

    context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    url = update.message.photo[-1].get_file().file_path

    rs = requests.get(url)

    progress_message.edit_text(msg + '\n⬛⬛⬛⬜⬜')

    file_name = get_file_name_image(chat_id)
    with open(file_name, 'wb') as f:
        f.write(rs.content)

    msg = 'Картинка скачана!'
    log.debug(msg)
    progress_message.edit_text(msg + '\n⬛⬛⬛⬛⬛')
    progress_message.delete()

    update.message.reply_text(
        "Теперь доступны команды над картинкой!",
        reply_markup=REPLY_KEYBOARD_MARKUP
    )


def on_error(update: Update, context: CallbackContext):
    log.exception('Error: %s\nUpdate: %s', context.error, update)
    update.message.reply_text(config.ERROR_TEXT)


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

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text, on_request))
    dp.add_handler(MessageHandler(Filters.photo, on_photo))

    # log all errors
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
