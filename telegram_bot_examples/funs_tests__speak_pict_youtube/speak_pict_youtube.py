#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import random
import sys
import time
import os
from pathlib import Path

from telegram import Update, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

sys.path.append('..')
sys.path.append('../../html_parsing')
sys.path.append('../../exchange_rates')

import config
from common import get_logger, log_func, reply_error
from cbr_ru import exchange_rate
from youtube_com__results_search_query import search_youtube


ALL_COMMANDS = []

log = get_logger(__file__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext):
    update.effective_message.reply_text(text='Hi!')


def help(update: Update, context: CallbackContext):
    text = 'Commands:\n' + '\n'.join(f'    /{x}' for x in ALL_COMMANDS)
    update.effective_message.reply_text(text)


def echo(update: Update, context: CallbackContext):
    message = update.effective_message
    message.reply_text(text=f'Echo: {message.text}')


def on_exchange_rates(update: Update, context: CallbackContext):
    text = 'Курс:'
    for code in ['USD', 'EUR']:
        text += f'\n    {code}: {exchange_rate(code)[0]}'

    log.debug(text)
    update.effective_message.reply_text(text=text)


def pict(update: Update, context: CallbackContext):
    update.effective_message.reply_photo('https://t8.mangas.rocks/auto/07/48/88/Onepunchman_t1_gl1_18.png')


def pict2(update: Update, context: CallbackContext):
    message = update.effective_message
    
    with open('files/Onepunchman_t1_gl1_18.png', 'rb') as f:
        message.reply_photo(f)


def pict3(update: Update, context: CallbackContext):
    message = update.effective_message

    max_parts = 10
    files = list(Path('files/readmanga.live_one_punch_man__A1bc88e_vol1_1').glob('*.*'))

    media_groups = []
    for i in range(0, len(files), max_parts):
        media = [
            InputMediaPhoto(f.open('rb')) for f in files[i: i+max_parts]
        ]
        media_groups.append(media)

    for i, media_group in enumerate(media_groups, 1):
        if len(media_groups) > 1:
            media_groups[0][0].caption = f'Часть #{i}'

        message.reply_media_group(media_group)


# Поиск на YouTube
def video(update: Update, context: CallbackContext):
    message = update.effective_message

    args = context.args
    log.debug(args)
    if not args:
        message.reply_text(text='К команде добавьте запрос.')
        return

    msg = ' '.join(args)
    search_results = search_youtube(msg)
    if not search_results:
        message.reply_text(text='Ничего не найдено.')
        return

    url, title = random.choice(search_results)
    message.reply_text(text=title + '\n' + url)


# NOTE: not work, source: https://github.com/gil9red/SimplePyScripts/blob/b366323934eb0ed9557ba7d40c3c64cf6a7b8c36/speak__[does_not_work]
# locale = 'ru-RU'
# gender = 'female'
#
#
# def speak(update: Update, context: CallbackContext):
#     args = context.args
#     log.debug(args)
#
#     if not args:
#         # log.debug('Список пуст')
#         # return
#         args = ['Сорок тысяч обезьян в жопу сунули банан']
#
#     def bing_speak(text, locale, gender):
#         """
#         Функция выполняет запрос в bing сервис синтезирования речи и возвращает получившийся mp3-файл с речью
#         в виде байтовой строки.
#
#         """
#
#         # Примеры запросов в сервис синтезирования речи:
#         # http://www.bing.com/translator/api/language/Speak?locale=ru-RU&gender=male&media=audio/mp3&text=gil9red+%D0%BA%D0%BB%D0%B5%D0%B2%D1%8B%D0%B9+%D1%87%D1%83%D0%B2%D0%B0%D0%BA
#         # http://www.bing.com/translator/api/language/Speak?locale=ru-RU&gender=female&media=audio/mp3&text=gil9red+%D0%BA%D0%BB%D0%B5%D0%B2%D1%8B%D0%B9+%D1%87%D1%83%D0%B2%D0%B0%D0%BA
#
#         url = 'https://www.bing.com/translator/api/language/Speak'
#         params = {
#             'locale': locale,
#             'gender': gender,
#             'media': 'audio/mp3',
#             'text': text,
#         }
#
#         s = requests.Session()
#
#         # Получим куки, иначе получим ошибку: {"message": "Service unavailable. Please try again later."}
#         rs = s.get('http://www.bing.com/translator')
#         if not rs.ok:
#             raise Exception('Error [%s]: %s.', rs.status_code, rs.text)
#
#         rs = s.get(url, params=params)
#         if not rs.ok:
#             raise Exception('Error [%s]: %s.', rs.status_code, rs.text)
#
#         return rs.content
#
#     # with open('OP_836_page02.png', 'rb') as f:
#
#     # Первый элемент args -- текст
#     # Второй голос
#     # Третий локаль
#     #
#     text = ' '.join(args)
#     mp3_content = bing_speak(text, locale, gender)
#
#     # Сохраняем в файл и возвращаем объект для считывания
#     with open('speak.mp3', 'wb') as f:
#         f.write(mp3_content)
#
#         with open('speak.mp3', 'rb') as f:
#             message.reply_audio(message.chat_id, audio=f, title='Speak {} {}'.format(gender, locale))
#
#
# def speak_set_locale(update: Update, context: CallbackContext):
#     log.debug('speak_set_locale')
#     args = context.args
#     if not args:
#         # TODO: писать об ошиюке в чат
#         log.debug('Список пуст')
#         return
#
#     global locale
#     last_locale = locale
#     locale = args[0]
#
#     message.reply_text(text='Speak locale изменена: {} -> {}.'.format(last_locale, locale))
#
#
# def speak_set_gender(update: Update, context: CallbackContext):
#     log.debug('speak_set_gender')
#     args = context.args
#     if not args:
#         # TODO: писать об ошиюке в чат
#         log.debug('Список пуст')
#         return
#
#     global gender
#     last_gender = gender
#     gender = args[0]
#
#     message.reply_text(text='Speak gender изменена: {} -> {}.'.format(last_gender, gender))


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

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("hi", lambda update, context: update.message.reply_text(text='hi')))
    dp.add_handler(CommandHandler("say", lambda update, context: update.message.reply_text(text=f'''I say: "{" ".join(context.args)}".''')))
    dp.add_handler(CommandHandler("exchange_rates", on_exchange_rates))
    dp.add_handler(CommandHandler("pict", pict))
    dp.add_handler(CommandHandler("pict2", pict2))
    dp.add_handler(CommandHandler("pict3", pict3))
    dp.add_handler(CommandHandler("yt", video))

    # NOTE: not work
    # dp.add_handler(CommandHandler("speak", speak))
    # dp.add_handler(CommandHandler("speak_set_locale", speak_set_locale))
    # dp.add_handler(CommandHandler("speak_set_gender", speak_set_gender))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    for commands in dp.handlers.values():
        for command in commands:
            if isinstance(command, CommandHandler):
                ALL_COMMANDS.extend(command.command)

    # log all errors
    dp.add_error_handler(on_error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    while True:
        try:
            main()
        except:
            log.exception('')

            timeout = 15
            log.info(f'Restarting the bot after {timeout} seconds')
            time.sleep(timeout)
