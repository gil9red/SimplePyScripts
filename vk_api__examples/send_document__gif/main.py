#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# Чтобы можно было импортировать config.py, находящийся уровнем выше
import sys
sys.path.append('..')

from config import LOGIN, PASSWORD


def upload_doc(file_name):
    import vk_api
    upload = vk_api.VkUpload(vk)
    rs = upload.document(file_name)

    # Составление названия документа: https://vk.com/dev/messages.send
    attachment = 'doc{owner_id}_{id}'.format(**rs[0])
    return attachment


if __name__ == '__main__':
    import vk_api
    vk = vk_api.VkApi(login=LOGIN, password=PASSWORD)
    vk.auth()

    # Получаем информацию о самом себе
    rs = vk.method('users.get')
    user_id = rs[0]['id']

    file_name = 'file_name.gif'

    vk.method('messages.send', {
        'user_id': user_id,
        # 'message': 'Doc:',
        'attachment': upload_doc(file_name),
    })
