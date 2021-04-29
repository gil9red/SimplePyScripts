#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import json
import logging
import time
import sys

from datetime import datetime
from random import randint

import lxml.html
import requests
import vk_api

from urllib.parse import urljoin


def get_logger(name, file='log.txt', encoding='utf8', fmt=None):
    fmt = '[%(asctime)s] %(filename)s[LINE:%(lineno)d] %(levelname)-8s %(message)s' if fmt is None else fmt

    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter(fmt)

    fh = logging.FileHandler(file, encoding=encoding)
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(logging.DEBUG)

    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    log.addHandler(fh)
    log.addHandler(ch)

    return log


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
    except Exception as e:
        logger.exception("При авторизации произошла ошибка:")
        sys.exit()

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
    config = json.load(open('config.json'))

    # Логин, пароль к аккаунту и id человека, на стену которого будем постить сообщения
    login = config['login']
    password = config['password']
    to = config['to']
    quote_count = config['quote_count']
    at = config['at']

    logger = get_logger('vk_spam_wall', fmt=config['logging_format'])
    logger.debug('Конфиг: %s.', config)
    logger.debug('Начало работы.')

    if not login or not password:
        logger.error('Логин/пароль не указаны.')
        sys.exit()

    # Авторизируемся
    vk = vk_auth(login, password)

    # Если определен, то узнаем id пользователя которого будем спамить, иначе шлем самим себе
    if to:
        rs = vk.method('users.get', dict(user_ids=to))[0]
        owner_id = int(rs['id'])
    else:
        owner_id = None

    at_time = datetime.strptime(at, '%H:%M').time()
    # dt = datetime.combine(datetime.today(), at_time) + timedelta(minutes=70)
    # at_time = dt.time()

    while True:
        # Ждем наступления времени, указанного в at
        while True:
            # Убираем микросекунды, иначе совпадения вряд ли дождемся в этой жизни
            now = datetime.today().time()
            now = now.replace(now.hour, now.minute, microsecond=0)
            if now == at_time:
                break

            time.sleep(0.5)

        delay = randint(0, 60 * 4)
        logger.debug('Время выполнения наступило. Жду %s секунд.', delay)

        # Случайно ждем от 0 до 240 секунд
        time.sleep(delay)

        try:
            # Начинаем постить на стену
            for href in bash_quote(count=quote_count):
                wall_post(vk, owner_id, href)

                # Ждем от 2 до 5 минут + 0 до 60 секунд
                interval = randint(2, 5) * 60 + randint(0, 60)
                logger.debug('До следующего постинга осталось %s секунд.', interval)
                time.sleep(interval)

        except Exception as e:
            logger.exception("Произошла ошибка:")
