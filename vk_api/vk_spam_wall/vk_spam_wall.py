#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from datetime import datetime, timedelta
import json
import lxml.html
import logging
import time
from urllib.parse import urljoin
from random import randint
import sys

import requests
import vk_api


def get_logger(name, file='log.txt', encoding='utf8'):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] %(filename)s[LINE:%(lineno)d] %(levelname)-8s %(message)s')

    fh = logging.FileHandler(file, encoding=encoding)
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(logging.DEBUG)

    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    log.addHandler(fh)
    log.addHandler(ch)

    return log


logger = get_logger('vk_spam_wall')


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
        logger.debug('Авторизуюсь в vk.')
        vk.authorization()
    except vk_api.AuthorizationError as e:
        logger.error('При авторизации произошла ошибка: %s.', e)
        quit()

    logger.debug('Удачная авторизация.')

    return vk


def wall_post(vk, owner_id, quote_href):
    logger.debug('Размещаю сообщение на стену.')

    # Добавление сообщения на  стену пользователя (owner_id это id пользователя)
    # Если не указывать owner_id, сообщения себе на стену поместится
    rs = vk.method('wall.post', {
        'owner_id': owner_id,
        'attachments': quote_href,
    })

    logger.debug('post_id: %s, quote href: %s.', rs['post_id'], quote_href)


if __name__ == '__main__':
    logger.debug('Начало работы.')
    logger.debug('Читаю файл конфига.')

    config = json.load(open('config.json'))

    # Логин, пароль к аккаунту и id человека, на стену которого будем постить сообщения
    login = config['login']
    password = config['password']
    to = config['to']
    quote_count = config['quote_count']

    logger.debug('Закончено чтение файла конфига. Конфиг: %s.', config)

    if not login or not password:
        logger.error('Логин/пароль не указаны.')
        quit()

    # Авторизируемся
    vk = vk_auth(login, password)

    # Если определен, то узнаем id пользователя которого будем спамить, иначе шлем самим себе
    if to:
        rs = vk.method('users.get', dict(user_ids=to))[0]
        owner_id = int(rs['id'])
    else:
        owner_id = None

    while True:
        try:
            for href in bash_quote(count=quote_count):
                wall_post(vk, owner_id, href)

                # Ждем от 2 до 5 минут + 0 до 60 секунд
                interval = randint(2, 5) * 60 + randint(0, 60)
                logger.debug('До следующего постинга осталось %s секунд.', interval)
                time.sleep(interval)

        except Exception as e:
            print('Что-то пошло не так :( -- "{}"'.format(e))

        # Ждем от 24 часов до 28 часов
        interval = randint(24 * 3600, 28 * 3600)
        d = datetime.now() + timedelta(seconds=interval)
        logger.debug('Следующий раз пошлем через {} секунд (в {:%Y-%m-%d %H:%M:%S}).'.format(interval, d))

        # В следующий раз п пошлем
        time.sleep(interval)
