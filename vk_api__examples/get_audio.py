#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from vk_api.audio import VkAudio
from root_common import get_vk_session


vk_session = get_vk_session()
vk_audio = VkAudio(vk_session)

audio_list = vk_audio.get()

print(f"Audio list ({len(audio_list)}):")
for i, audio in enumerate(audio_list, 1):
    title = audio["title"]
    artist = audio["artist"]
    duration = audio["duration"]
    url = audio["url"]
    print(f"    {i}. {title!r} by {artist!r}, duration: {duration} secs, url: {url}")
