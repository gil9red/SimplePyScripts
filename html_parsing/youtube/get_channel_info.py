#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
from dataclasses import asdict

from api.channel import get_original_url, get_channel_info


url = get_original_url("https://www.youtube.com/c/Kuplinov")
assert url == "https://www.youtube.com/c/Kuplinov"

url = get_original_url(
    "https://www.youtube.com/redirect?event=channel_description"
    "&redir_token=QUFFLUhqbXI5V01wbEF1eGlqUzZsdkczWnFEUk1fWlV5QX"
    "xBQ3Jtc0tsUUVsY2hyQncxeVhzTVNKV1JpOWdxbDZVWEtKRy00OG5kZVlBZ"
    "TlTM2FqLUhhMlhpcVhRMk9xTHc2cjdjRzlUTTFYYTdCNVU4VE1GZHNoMVFj"
    "Q09HcnhWcV8xOVJiZjFtQlVSMkFwU1JORjB5QzVUbw"
    "&q=https%3A%2F%2Ft.me%2FKuplinov_Telegram"
)
assert url == "https://t.me/Kuplinov_Telegram"

channel_info = get_channel_info("https://www.youtube.com/@kuplinovplay")
print(channel_info)
# ChannelInfo(channel_id='UCdKuE7a2QZeHPhDntXVZ91w', canonical_channel_url='http://www.youtube.com/@kuplinovplay', description='Здесь можно поржать, отложить кирпичей, снять стресс и сбросить вес.', subscriber_count_text='16,9 млн подписчиков', view_count_text='6 880 видео', joined_date_text='Дата регистрации: 23 дек. 2012 г.', links=[Link(title='Telegram', url='https://t.me/Kuplinov_Telegram'), Link(title='Почта для деловых предложений', url='kuplinov.partnership@mail.ru'), Link(title='VK', url='http://vk.com/dmitry.kuplinov'), Link(title='Паблик VK', url='http://vk.com/kuplinovplay'), Link(title='Второй канал', url='https://www.youtube.com/c/Kuplinov')])

print(json.dumps(asdict(channel_info), ensure_ascii=False, indent=4))
"""
{
    "channel_id": "UCdKuE7a2QZeHPhDntXVZ91w",
    "canonical_channel_url": "http://www.youtube.com/@kuplinovplay",
    "description": "Здесь можно поржать, отложить кирпичей, снять стресс и сбросить вес.",
    "subscriber_count_text": "16,9 млн подписчиков",
    "view_count_text": "6 880 видео",
    "joined_date_text": "Дата регистрации: 23 дек. 2012 г.",
    "links": [
        {
            "title": "Telegram",
            "url": "https://t.me/Kuplinov_Telegram"
        },
        {
            "title": "Почта для деловых предложений",
            "url": "kuplinov.partnership@mail.ru"
        },
        {
            "title": "VK",
            "url": "http://vk.com/dmitry.kuplinov"
        },
        {
            "title": "Паблик VK",
            "url": "http://vk.com/kuplinovplay"
        },
        {
            "title": "Второй канал",
            "url": "https://www.youtube.com/c/Kuplinov"
        }
    ]
}
"""

print()

for link in channel_info.links:
    print(link)
"""
Link(title='Telegram', url='https://t.me/Kuplinov_Telegram')
Link(title='Почта для деловых предложений', url='kuplinov.partnership@mail.ru')
Link(title='VK', url='http://vk.com/dmitry.kuplinov')
Link(title='Паблик VK', url='http://vk.com/kuplinovplay')
Link(title='Второй канал', url='https://www.youtube.com/c/Kuplinov')
"""
