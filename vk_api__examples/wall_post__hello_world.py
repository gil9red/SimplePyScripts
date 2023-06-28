#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = "ipetrash"


from root_common import get_vk_session


OWNER_ID = None


vk_session = get_vk_session()
vk = vk_session.get_api()

# Добавление сообщения на стену пользователя (owner_id это id пользователя)
# Если не указывать owner_id, то сообщение будет отправлено себе на стену
rs = vk.wall.post(
    owner_id=OWNER_ID,
    message="Hello World!\nПривет мир!",
)
print("rs:", rs)
