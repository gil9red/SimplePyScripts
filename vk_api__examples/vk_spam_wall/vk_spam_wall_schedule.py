#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import json
import logging
import time
import sys

from datetime import datetime, timedelta
from urllib.parse import urljoin
from random import randint

import lxml.html
import requests
import vk_api
import schedule


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

    hrefs = []
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
        sys.exit()

    logger.debug('Удачная авторизация.')
    return vk


def wall_post(vk, owner_id, quote_href):
    logger.debug('Размещаю сообщение на стену.')

    # Добавление сообщения на  стену пользователя (owner_id это id пользователя)
    # Если не указывать owner_id, сообщения себе на стену поместится
    rs = vk.method('wall.post', {
        'owner_id': int(owner_id) if owner_id else None,
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
    at = config['at']
    quote_count = config['quote_count']

    logger.debug('Закончено чтение файла конфига. Конфиг: %s.', config)

    if not login or not password:
        logger.error('Логин/пароль не указаны.')
        sys.exit()

    # Авторизируемся
    vk = vk_auth(login, password)

    str_at_time = at

    try:
        for href in bash_quote(count=quote_count):
            # schedule.clear()

            logger.debug('Задача запланирована на %s.', str_at_time)
            schedule.every().day.at(str_at_time).do(wall_post, vk=vk, owner_id=to, quote_href=href)

            # Следующая задача выполнится чуть позже
            at_time = time.strptime(str_at_time, '%H:%M')
            at_time = timedelta(hours=at_time.tm_hour, minutes=at_time.tm_min)
            at_time += timedelta(minutes=randint(2, 5), seconds=randint(0, 60))
            str_at_time = (datetime.min + at_time).strftime('%H:%M')

        while True:
            schedule.run_pending()
            time.sleep(1)

    except Exception as e:
        print('Что-то пошло не так :( -- "{}"'.format(e))
