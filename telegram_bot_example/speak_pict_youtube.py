#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


TOKEN = '<TOKEN>'


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')


def echo(bot, update):
    bot.sendMessage(update.message.chat_id, text=update.message.text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


# TODO: правильное название функции
def curs(bot, update):
    import requests

    rs = requests.get('https://query.yahooapis.com/v1/public/yql?q=select+*+from+yahoo.finance.xchange+where+pair+=+%22USDRUB,EURRUB%22&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback=')

    text = 'Курс:'
    for rate in rs.json()['query']['results']['rate']:
        text += '\n' + rate['Name'].split('/')[0] + ' ' + rate['Rate']

    print(text)
    bot.sendMessage(update.message.chat_id, text=text)


def pict(bot, update):
    bot.sendPhoto(update.message.chat_id, 'http://e3.postfact.ru/auto/18/91/16/OP_836_page01.png')


def pict2(bot, update):
    with open('OP_836_page02.png', 'rb') as f:
        bot.sendPhoto(update.message.chat_id, f)


#
#
# Поиск на YouTube
def video(bot, update, args):
    print(args)
    if not args:
        bot.sendMessage(update.message.chat_id, text='К команде добавьте запрос.')
        return

    msg = ' '.join(args)

    import urllib
    import re
    import random
    from telegram import ParseMode

    link = urllib.parse.urlencode({"search_query": msg})
    content = urllib.request.urlopen("https://www.youtube.com/results?" + link)
    search_results = re.findall('href=\"\/watch\?v=(.*?)\"', content.read().decode())
    if len(search_results)>0:
        # Первые 10 результатов
        search_results = search_results[0:9:1]
        choice_f = random.choice(search_results)
        yt_link = "https://www.youtube.com/watch?v="+choice_f
        bot.sendMessage(update.message.chat_id, text=yt_link, parse_mode=ParseMode.MARKDOWN)
    else:
        bot.sendMessage(update.message.chat_id, text='Ничего не найдено.')


locale = 'ru-RU'
gender = 'female'


# TODO:
def speak(bot, update, args):
    print(args)

    if not args:
        # # TODO: писать об ошиюке в чат
        # print('Список пуст')
        # return
        args = ['Сорок тысяч обезьян в жопу сунули банан']

    def bing_speak(text, locale, gender):
        """
        Функция выполняет запрос в bing сервис синтезирования речи и возвращает получившийся mp3-файл с речью
        в виде байтовой строки.

        """

        # Примеры запросов в сервис синтезирования речи:
        # http://www.bing.com/translator/api/language/Speak?locale=ru-RU&gender=male&media=audio/mp3&text=gil9red+%D0%BA%D0%BB%D0%B5%D0%B2%D1%8B%D0%B9+%D1%87%D1%83%D0%B2%D0%B0%D0%BA
        # http://www.bing.com/translator/api/language/Speak?locale=ru-RU&gender=female&media=audio/mp3&text=gil9red+%D0%BA%D0%BB%D0%B5%D0%B2%D1%8B%D0%B9+%D1%87%D1%83%D0%B2%D0%B0%D0%BA

        url = 'http://www.bing.com/translator/api/language/Speak'
        params = {
            'locale': locale,
            'gender': gender,
            'media': 'audio/mp3',
            'text': text,
        }

        import requests
        s = requests.Session()

        # Получим куки, иначе получим ошибку: {"message": "Service unavailable. Please try again later."}
        rs = s.get('http://www.bing.com/translator')
        if not rs.ok:
            raise Exception('Error [%s]: %s.', rs.status_code, rs.text)

        rs = s.get(url, params=params)
        if not rs.ok:
            raise Exception('Error [%s]: %s.', rs.status_code, rs.text)

        return rs.content

    # with open('OP_836_page02.png', 'rb') as f:

    # Первый элемент args -- текст
    # Второй голос
    # Третий локаль
    #
    text = ' '.join(args)
    mp3_content = bing_speak(text, locale, gender)

    # TODO: выглядит костыльно
    # Сохраняем в файл и возвращаем объект для считывания
    with open('speak.mp3', 'wb') as f:
        f.write(mp3_content)

        with open('speak.mp3', 'rb') as f:
            bot.sendAudio(update.message.chat_id, audio=f, title='Speak {} {}'.format(gender, locale))


def speak_set_locale(bot, update, args):
    print('speak_set_locale')
    if not args:
        # TODO: писать об ошиюке в чат
        print('Список пуст')
        return

    global locale
    last_locale = locale
    locale = args[0]

    bot.sendMessage(update.message.chat_id, text='Speak locale изменена: {} -> {}.'.format(last_locale, locale))


def speak_set_gender(bot, update, args):
    print('speak_set_gender')
    if not args:
        # TODO: писать об ошиюке в чат
        print('Список пуст')
        return

    global gender
    last_gender = gender
    gender = args[0]

    bot.sendMessage(update.message.chat_id, text='Speak gender изменена: {} -> {}.'.format(last_gender, gender))


if __name__ == '__main__':
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("HI", lambda bot, update: bot.sendMessage(update.message.chat_id, text='HIII!')))
    dp.add_handler(CommandHandler("hi", lambda bot, update: bot.sendMessage(update.message.chat_id, text='hi')))
    dp.add_handler(CommandHandler("say", lambda bot, update, args: bot.sendMessage(update.message.chat_id, text='I say: "{}".'.format(args)), pass_args=True))
    dp.add_handler(CommandHandler("curs", curs))
    dp.add_handler(CommandHandler("pict", pict))
    dp.add_handler(CommandHandler("pict2", pict2))
    dp.add_handler(CommandHandler("yt", video, pass_args=True))

    dp.add_handler(CommandHandler("speak", speak, pass_args=True))
    dp.add_handler(CommandHandler("speak_set_locale", speak_set_locale, pass_args=True))
    dp.add_handler(CommandHandler("speak_set_gender", speak_set_gender, pass_args=True))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler([Filters.text], echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
