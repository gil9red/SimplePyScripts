#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# Пример отправки самому себе сообщения


import vk_api

import logging
import traceback
import datetime
import time
import sys


def get_logger(name, file='log.txt', encoding='utf8'):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] %(filename)s[LINE:%(lineno)d] %(levelname)-8s %(message)s')

    if file is not None:
        fh = logging.FileHandler(file, encoding=encoding)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        log.addHandler(fh)

    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    log.addHandler(ch)

    return log


def new_guid():
    now = datetime.datetime.now().timetuple()
    return int(time.mktime(now))


def send_message(text, user_id):
    values = {
        'user_id': user_id,
        'message': text,
        'guid': new_guid(),
    }

    logger.debug('Execute vk method messages.send with values: {}'.format(values))
    result = vk.method('messages.send', values=values)
    logger.debug('Result: {}'.format(result))

    return result


logger = get_logger('selfie_send')


LOGIN = ''
PASSWORD = ''

# Id пользователя, которому пошлем сообщение
USER_ID = None

assert LOGIN and PASSWORD and USER_ID is not None, "Логин, пароль и user_id должны быть указаны"


if __name__ == '__main__':
    try:
        logger.debug('Vk authorization')

        vk = vk_api.VkApi(LOGIN, PASSWORD)
        vk.authorization()  # Авторизируемся

        send_message('Hello! Привет!\nYahoo!', USER_ID)

    except Exception as e:
        logger.error('{}\n{}'.format(e, traceback.format_exc()))
        exit()
