#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# Аналог: http://habrahabr.ru/post/244647/ ( Делаем дамп фотографий из диалога vk.com )

import os
import time
import traceback
from urllib.request import urlretrieve
from urllib.error import HTTPError

import vk_api


import logging
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


def get_history(offset, count_step, user_id):
    logger.debug('get_history: offset={} count_step={} user_id={}'.format(offset, count_step, user_id))

    values = {
        'offset': offset,
        'count': count_step,
        'user_id': user_id,
        'rev': 1,
    }

    logger.debug('Execute vk method messages.getHistory with values: {}'.format(values))
    history = vk.method('messages.getHistory', values=values)

    # Чтобы контакт не ругался на слишком частые запросы
    time.sleep(0.3)

    offset += count_step
    total_messages = history['count']

    upload_precent = offset / total_messages * 100
    upload_precent = 100 if upload_precent > 100 else upload_precent

    # Перебор сообщений в диалоге
    for mess in history['items']:
        logger.debug('Message id={} text="{}"'.format(mess['id'], mess['body']))

        # Если есть прикрепленные данные
        if 'attachments' in mess:
            # Фильтруем, нам нужны только фотографии
            photo_list = [x['photo'] for x in mess['attachments'] if x['type'] == 'photo']

            # Если список фотографий не пуст
            if photo_list:
                logger.debug('Attachment photos ({}):'.format(len(photo_list)))

                for photo in photo_list:
                    logger.debug('Photos: {}'.format(photo))
                    # TODO: в сообщения указывать отпрравителя и дату отправки
                    # TODO: некоторые фотографии временно недоступны в данный момент, вк вместо их url
                    # присылает http://vk.com/images/x_null.gif, для каждого размера gif префикс перед _null
                    # отличается
                    # TODO: доставать по указанному размеру, т.к. варианты размеров предопределены:
                    # photo_75 	url копии фотографии с максимальным размером 75x75px.
                    # photo_130 	url копии фотографии с максимальным размером 130x130px.
                    # photo_604 	url копии фотографии с максимальным размером 604x604px.
                    # photo_807 	url копии фотографии с максимальным размером 807x807px.
                    # photo_1280 	url копии фотографии с максимальным размером 1280x1024px.
                    # photo_2560 	url копии фотографии с максимальным размером 2560x2048px.
                    # TODO: или хитрее действовать -- берем максимальный размер, и если указаны
                    # параметры width и height (они могут не быть в старых фотографиях), то подгоняем
                    # изображение до оригинального размера

                    # Photo содержит несколько url'ов -- на разные размеры изображений, мы возьмем
                    # самвй большой, для этого, вытащим все ключи с ссылками на изображения,
                    # отсортируем по размерам получившийся список и url последним ключом из списка (самый
                    # большой размер картинки)
                    photo_size_keys = [x for x in photo.keys() if 'photo_' in x]
                    photo_size_keys = sorted(photo_size_keys, key=lambda x: int(x.split('_')[1]))
                    key_big_size = photo_size_keys[-1]
                    photo_url = photo[key_big_size]

                    file_name = os.path.join(DOWNLOAD_DIR, os.path.basename(photo_url))

                    if 'width' in photo and 'height' in photo:
                        logger.debug('Save photo in {} (orig {}x{}): vk size={} url={}'.format(file_name,
                                                                                               photo['width'],
                                                                                               photo['height'],
                                                                                               key_big_size,
                                                                                               photo_url))
                    else:
                        logger.debug('Save photo in {}: vk size={} url={}'.format(file_name,
                                                                                  key_big_size,
                                                                                  photo_url))

                    # TODO: название можно брать осмысленное: например {id}_{time}_{size}.jpg
                    urlretrieve(photo_url, file_name)

    logger.debug('Progress {:.2f}%'.format(upload_precent))

    return offset, total_messages


logger = get_logger('download_vk_photo')


LOGIN = ''
PASSWORD = ''

# Id пользователя, с кем выдется диалог, из которого будем вытаскивать фотографии
USER_ID = None
DOWNLOAD_DIR = 'images_{}'.format(USER_ID)


assert LOGIN and PASSWORD and USER_ID is not None, "Логин, пароль и user_id должны быть указаны"

if not os.path.exists(DOWNLOAD_DIR):
    os.mkdir(DOWNLOAD_DIR)

if __name__ == '__main__':
    try:
        vk = vk_api.VkApi(LOGIN, PASSWORD)
        vk.authorization()  # Авторизируемся

        total_messages = 0
        count_step = 200
        offset = 0

        offset, total_messages = get_history(offset, count_step, USER_ID)

        logger.debug('Total messages: {}'.format(total_messages))

        # Вызываем функцию пока не переберем все сообщения данного диалога
        while offset < total_messages:
            try:
                offset, total_messages = get_history(offset, count_step, USER_ID)
            except (vk_api.ApiError, HTTPError) as e:
                logger.error('{}\n{}'.format(e, traceback.format_exc()))
                logger.debug('Waiting 60 seconds')
                time.sleep(60)

    except Exception as e:
        logger.error('{}\n{}'.format(e, traceback.format_exc()))
        sys.exit()
