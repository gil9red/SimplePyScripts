#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from config import LOGIN, PASSWORD

import vk_api
vk_session = vk_api.VkApi(login=LOGIN, password=PASSWORD)
vk_session.auth()

vk = vk_session.get_api()
owner_id = vk.users.get()[0]['id']

from vk_api.audio import VkAudio
vk_audio = VkAudio(vk_session)

# Без использования offset не получить все, если их больше 50
audio_list = vk_audio.get(owner_id=owner_id)

print('Audio list ({}):'.format(len(audio_list)))
for i, audio in enumerate(audio_list, 1):
    print('    {0}. "{1[title]}" by "{1[artist]}", duration: {1[dur]} secs, url: {1[url]}'.format(i, audio))
