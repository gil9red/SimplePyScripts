#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from common import Video


url = "https://www.youtube.com/watch?v=OIVXORUjzTE"

video = Video.get_from(url)
print(video)
# Video(id='OIVXORUjzTE', url='https://www.youtube.com/watch?v=OIVXORUjzTE', title='The Corridor Прохождение ► Прямоугольная теория ► ИНДИ-ХОРРОР', duration_seconds=612, duration_text='00:10:12', seq=None, is_live_now=False)

print()

number = 0

print("Transcripts:")
for transcript in video.get_transcripts():
    print(transcript)
    number += transcript.text.count("[\xa0__\xa0]")
"""
Transcripts:
TranscriptItem(start_ms=800, end_ms=3449, start_time_str='0:00', text='всем привет друзья меня зовут дмитрий')
TranscriptItem(start_ms=3449, end_ms=6720, start_time_str='0:03', text='это канал куплинов play и сейчас мы')
TranscriptItem(start_ms=6720, end_ms=10650, start_time_str='0:06', text='будем играть в коридор что гласит нам')
TranscriptItem(start_ms=10650, end_ms=14099, start_time_str='0:10', text='название видать игра пара коридор хотя')
TranscriptItem(start_ms=14099, end_ms=16170, start_time_str='0:14', text='было бы странно если бы [\xa0__\xa0] игра')
...
TranscriptItem(start_ms=604930, end_ms=607600, start_time_str='10:04', text='пытаюсь это исправить всем пока буду')
TranscriptItem(start_ms=607600, end_ms=609430, start_time_str='10:07', text='всех ждать следующих видео и скоро')
TranscriptItem(start_ms=609430, end_ms=612750, start_time_str='10:09', text='увидимся пока')
"""

print()

print(f"Swear words: {number}")
print(
    f'Swear word about every {(video.duration_seconds // number) if number else "-"} seconds'
)
"""
Swear words: 28
Swear word about every 21 seconds
"""
