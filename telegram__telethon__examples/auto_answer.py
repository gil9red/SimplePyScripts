#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/LonamiWebs/Telethon
# SOURCE: https://my.telegram.org/apps


# pip install telethon
from telethon.sync import TelegramClient, events

from config import API_ID, API_HASH


with TelegramClient("my", API_ID, API_HASH) as client:

    @client.on(events.NewMessage(from_users=[321346650, 257199860]))
    async def handler(event):
        print(event)
        await event.reply("Сейчас не могу ответить 😔")

    client.run_until_disconnected()
