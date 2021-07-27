#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import glob
import sys
import random

from pathlib import Path
from typing import List, Union

from vk_api.upload import VkUpload

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent.parent
sys.path.append(str(ROOT_DIR))
from root_common import get_vk_session


def upload_images(upload: VkUpload, file_names: Union[str, List[str]]) -> str:
    rs = upload.photo_messages(file_names)

    # Составление названия изображений: https://vk.com/dev/messages.send
    return ','.join(f"photo{item['owner_id']}_{item['id']}" for item in rs)


USER_ID = None


if __name__ == '__main__':
    vk_session = get_vk_session()
    upload = VkUpload(vk_session)

    # Берем все картинки
    file_names = glob.glob('*.png')

    vk_session.method('messages.send', {
        'user_id': USER_ID,
        'message': 'All:',
        'attachment': upload_images(upload, file_names),
    })

    file_name = random.choice(file_names)
    vk_session.method('messages.send', {
        'user_id': USER_ID,
        'message': 'Random:',
        'attachment': upload_images(upload, file_name),
    })
