#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from root_common import get_vk_session


# Указывать id пользоваля или его короткое имя
USER_ID = None


vk_session = get_vk_session()
vk = vk_session.get_api()

rs = vk.users.get(user_ids=USER_ID)[0]
print(rs)
