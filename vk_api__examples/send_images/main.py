#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
import requests
import json
import vk_auth

# Ваши данные ВК
email = ''
password = ''
client_id = ''
# Необходимые нам права
scope = 'wall,photos'
# Идентификаторы группы
gid = ''

token = vk_auth(email, password, client_id, scope)[0]

# путь к вашему изображению
img = {'photo': ('img.jpg', open(r'img.jpg', 'rb'))}

# Получаем ссылку для загрузки изображений
method_url = 'https://api.vk.com/method/photos.getWallUploadServer?'
data = dict(access_token=token, gid=gid)
response = requests.post(method_url, data)
result = json.loads(response.text)
upload_url = result['response']['upload_url']

# Загружаем изображение на url
response = requests.post(upload_url, files=img)
result = json.loads(response.text)

# Сохраняем фото на сервере и получаем id
method_url = 'https://api.vk.com/method/photos.saveWallPhoto?'
data = dict(access_token=token, gid=gid, photo=result['photo'], hash=result['hash'], server=result['server'])
response = requests.post(method_url, data)
result = json.loads(response.text)['response'][0]['id']

# Теперь этот id остается лишь прикрепить в attachments метода wall.post
method_url = 'https://api.vk.com/method/wall.post?'
data = dict(access_token=token, owner_id='-' + gid, attachments=result, message='')
response = requests.post(method_url, data)
result = json.loads(response.text)

# На выходе мы получим в ответе post_id если не было ошибки
"""


# Чтобы можно было импортировать config.py, находящийся уровнем выше
import sys
sys.path.append('..')

from config import LOGIN, PASSWORD


# def upload_image(vk, file_name):
#     img_data = {
#         'photo': (file_name, open(file_name, mode='rb'))
#     }
#
#     # Получение доступного сервера для загрузки
#     # https://vk.com/dev/photos.getMessagesUploadServer
#     rs = vk.method('photos.getMessagesUploadServer')
#     upload_url = rs['upload_url']
#
#     # Загрузка изображения на сервер
#     import requests
#     rs = requests.post(upload_url, files=img_data)
#
#     # Сохранение фото на сервере и получание его id
#     # https://vk.com/dev/photos.saveMessagesPhoto
#     rs = vk.method('photos.saveMessagesPhoto', rs.json())
#
#     # Составление названия изображения: https://vk.com/dev/messages.send
#     attachment_image = 'photo{owner_id}_{id}'.format(**rs[0])
#     return attachment_image


def upload_images(file_names):
    import vk_api
    upload = vk_api.VkUpload(vk)
    rs = upload.photo_messages(file_names)

    # Составление названия изображений: https://vk.com/dev/messages.send
    attachment_images = ','.join('photo{owner_id}_{id}'.format(**item) for item in rs)
    return attachment_images


if __name__ == '__main__':
    import vk_api
    vk = vk_api.VkApi(login=LOGIN, password=PASSWORD)
    vk.auth()

    # Получаем информацию о самом себе
    rs = vk.method('users.get')
    user_id = rs[0]['id']

    # Берем все картинки
    import glob
    file_names = glob.glob('*.png')

    vk.method('messages.send', {
        'user_id': user_id,
        'message': 'All:',
        'attachment': upload_images(file_names),
    })

    import random
    file_name = random.choice(file_names)

    vk.method('messages.send', {
        'user_id': user_id,
        'message': 'Random:',
        'attachment': upload_images(file_name),
    })
