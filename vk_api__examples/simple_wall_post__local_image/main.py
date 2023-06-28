#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
from pathlib import Path

from vk_api import VkUpload

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent
sys.path.append(str(ROOT_DIR))
from root_common import get_vk_session


# Посылаем себе на стену
OWNER_ID = None


vk_session = get_vk_session()
vk = vk_session.get_api()
upload = VkUpload(vk_session)  # Для загрузки изображений

photos = ["1.jpg", "2.jpg"]
# Или:
# photos = [open('1.jpg', 'rb'), open('2.jpg', 'rb')]

photo_list = upload.photo_wall(photos)
attachment = ",".join(f"photo{item['owner_id']}_{item['id']}" for item in photo_list)

vk_session.method(
    "wall.post",
    {
        "owner_id": OWNER_ID,
        "message": "Test #1!",
        "attachment": attachment,
    },
)

# Альтернатива использования vk_session.method:
# Позволяет обращаться к методам API как к обычным классам.
vk.wall.post(
    owner_id=OWNER_ID,
    message="Test #2!",
    attachment=attachment,
)
