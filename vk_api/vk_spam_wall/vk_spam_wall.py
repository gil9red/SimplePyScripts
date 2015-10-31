#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from datetime import datetime
import json
import lxml.html
import time
from urllib.parse import urljoin
from random import randint
import sys

import requests
import vk_api


def bash_quote(url='http://bash.im/', count=1):
    rs = requests.get(url)
    html = lxml.html.fromstring(rs.text)
    quotes = html.xpath('//div[@class="quote"]//a[@class="id"]')

    hrefs = list()

    for quote_href in quotes[:count]:
        quote_href = quote_href.attrib['href']
        quote_href = urljoin(rs.url, quote_href)
        hrefs.append(quote_href)

    return hrefs


def vk_auth(login, password):
    vk = vk_api.VkApi(login, password)

    try:
        # Авторизируемся
        vk.authorization()
    except vk_api.AuthorizationError as error_msg:
        print(error_msg)  # В случае ошибки выведем сообщение
        sys.exit()

    return vk


def wall_post(vk, owner_id, quote_href):
    # Добавление сообщения на  стену пользователя (owner_id это id пользователя)
    # Если не указывать owner_id, сообщения себе на стену поместится
    rs = vk.method('wall.post', {
        'owner_id': int(owner_id) if owner_id else None,
        'attachments': quote_href,
    })
    print('{}: post_id: {}, quote href: {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                   rs['post_id'], quote_href))


if __name__ == '__main__':
    config = json.load(open('config.json'))

    # Логин, пароль к аккаунту и id человека, на стену которого будем постить сообщения
    login = config['login']
    password = config['password']
    owner_id = config['owner_id']
    quote_count = config['quote_count']

    # Авторизируемся
    vk = vk_auth(login, password)

    while True:
        try:
            # Получаем 3 последние цитаты
            for href in bash_quote(count=quote_count):
                wall_post(vk, owner_id, href)

                # Ждем от 2 до 5 минут + 0 до 60 секунд
                interval = randint(2, 5) * 60 + randint(0, 60)
                print('До следующего постинга осталось {} секунд.'.format(interval))
                time.sleep(interval)

        except Exception as e:
            print('Что-то пошло не так :( -- "{}"'.format(e))

        # Ждем от 24 часов до 28 часов
        interval = randint(24 * 3600, 28 * 3600)
        print('\nСледующий раз пошлем через {} минут.\n'.format(interval))

        # В следующий раз п пошлем
        time.sleep(interval)
