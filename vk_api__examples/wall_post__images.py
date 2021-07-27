#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'ipetrash'


"""
Скрипт ищет картинки в инете и помещает на стену пользователя vk.com
"""


import sys
import random

from urllib.request import urlopen
from typing import List

from vk_api.upload import VkUpload

from root_config import DIR
from root_common import get_vk_session

# Для импортирования yandex_search_img.py
sys.path.append(str(DIR.parent))

from yandex_search_img import get_images


def get_attachments(upload: VkUpload, urls: List[str]) -> str:
    rs = upload.photo_wall([urlopen(url) for url in urls])
    return ','.join(f"photo{photo['owner_id']}_{photo['id']}" for photo in rs)


OWNER_ID = None

vk_session = get_vk_session()
vk = vk_session.get_api()
upload = VkUpload(vk_session)

text = 'Котята'
urls = get_images(text)

# "Перемешаем" элементы списка
random.shuffle(urls)

# Добавление сообщения на стену пользователя (owner_id это id пользователя)
# Если не указывать owner_id, то сообщение будет отправлено себе на стену
rs = vk.wall.post(
    owner_id=OWNER_ID,
    message=text + ' 3 шт.',
    attachments=get_attachments(upload, urls[:3]),
)
print('rs:', rs)

rs = vk.wall.post(
    owner_id=OWNER_ID,
    message=text + ' 1 шт.',
    attachments=get_attachments(upload, urls[:1]),
)
print('rs:', rs)
