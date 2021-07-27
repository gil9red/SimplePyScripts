#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Аналог: http://habrahabr.ru/post/244647/ (Делаем дамп фотографий из диалога vk.com)
"""


import os
import time
import sys

from pathlib import Path
from typing import Tuple
from urllib.error import HTTPError
from urllib.request import urlretrieve

import vk_api

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent.parent
sys.path.append(str(ROOT_DIR))
from root_common import get_vk_session, get_logger


def get_history(vk: vk_api.VkApi, offset: int, count_step: int, user_id: int = None) -> Tuple[int, int]:
    logger.debug(f'get_history: offset={offset} count_step={count_step} user_id={user_id}')

    values = {
        'offset': offset,
        'count': count_step,
        'user_id': user_id,
        'rev': 1,
    }

    logger.debug(f'Execute vk method messages.getHistory with values: {values}')
    history = vk.method('messages.getHistory', values=values)

    # Чтобы контакт не ругался на слишком частые запросы
    time.sleep(0.3)

    offset += count_step
    total_messages = history['count']

    upload_precent = offset / total_messages * 100
    upload_precent = 100 if upload_precent > 100 else upload_precent

    # Перебор сообщений в диалоге
    for mess in history['items']:
        logger.debug(f'Message id={mess["id"]} text={mess["body"]!r}')

        # Если есть прикрепленные данные
        if 'attachments' not in mess:
            continue

        # Фильтруем, нам нужны только фотографии
        photo_list = [x['photo'] for x in mess['attachments'] if x['type'] == 'photo']

        # Если список фотографий не пуст
        if not photo_list:
            continue

        logger.debug(f'Attachment photos ({len(photo_list)}):')

        for photo in photo_list:
            logger.debug(f'Photos: {photo}')

            # Photo содержит несколько url'ов - на разные размеры изображений, мы возьмем
            # самый большой, для этого, вытащим все ключи с ссылками на изображения,
            # отсортируем по размерам получившийся список и url последним ключом из списка (самый
            # большой размер картинки)
            photo_size_keys = [x for x in photo.keys() if 'photo_' in x]
            photo_size_keys = sorted(photo_size_keys, key=lambda x: int(x.split('_')[1]))
            key_big_size = photo_size_keys[-1]
            photo_url = photo[key_big_size]

            file_name = os.path.join(DOWNLOAD_DIR, os.path.basename(photo_url))

            if 'width' in photo and 'height' in photo:
                logger.debug(
                    f'Save photo in {file_name} (orig {photo["width"]}x{photo["height"]}): '
                    f'vk size={key_big_size} url={photo_url}'
                )
            else:
                logger.debug(f'Save photo in {file_name}: vk size={key_big_size} url={photo_url}')

            # TODO: название можно брать осмысленное: например {id}_{time}_{size}.jpg
            urlretrieve(photo_url, file_name)

    logger.debug(f'Progress {upload_precent:.2f}%')

    return offset, total_messages


logger = get_logger('download_vk_photo', DIR / 'log.txt')


# Id пользователя, с кем выдется диалог, из которого будем вытаскивать фотографии
USER_ID = None

DOWNLOAD_DIR = f'images_{USER_ID}'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


try:
    vk_session = get_vk_session()

    total_messages = 0
    count_step = 200
    offset = 0

    offset, total_messages = get_history(vk_session, offset, count_step, USER_ID)

    logger.debug(f'Total messages: {total_messages}')

    # Вызываем функцию пока не переберем все сообщения данного диалога
    while offset < total_messages:
        try:
            offset, total_messages = get_history(vk_session, offset, count_step, USER_ID)
        except (vk_api.ApiError, HTTPError) as e:
            logger.exception("Error:")
            logger.debug('Waiting 60 seconds')
            time.sleep(60)

except Exception as e:
    logger.exception("Error:")
    sys.exit()
