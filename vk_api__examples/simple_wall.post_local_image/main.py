#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import vk_api
from vk_api import VkUpload

# Авторизация по логину/паролю (если нужно по токену, заполнять параметр token)
login, password = '<login>', '<password>'

vk_session = vk_api.VkApi(login, password)
vk_session.auth()

upload = VkUpload(vk_session)  # Для загрузки изображений

photos = ['1.jpg', '2.jpg']
# Или:
# photos = [open('1.jpg', 'rb'), open('2.jpg', 'rb')]
photo_list = upload.photo_wall(photos)
attachment = ','.join('photo{owner_id}_{id}'.format(**item) for item in photo_list)

vk_session.method("wall.post", {
    'owner_id': None,  # Посылаем себе на стену
    'message': 'Test!',
    'attachment': attachment,
})

# Альтернатива использования vk_session.method:
# # Позволяет обращаться к методам API как к обычным классам.
# vk = vk_session.get_api()
# vk.wall.post(
#     owner_id=None,  # Посылаем себе на стену
#     message='Test!',
#     attachment=attachment,
# )
