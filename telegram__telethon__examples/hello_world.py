#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/LonamiWebs/Telethon
# SOURCE: https://my.telegram.org/apps


# pip install telethon
from telethon.sync import TelegramClient, events

from config import API_ID, API_HASH


with TelegramClient("my", API_ID, API_HASH) as client:
    client.send_message("me", "Hello, myself!")
    print("Picture big:", client.download_profile_photo("me"))
    print("Picture small:", client.download_profile_photo("me", download_big=False))

    @client.on(events.NewMessage(pattern="(?i).*Hello"))
    async def handler(event) -> None:
        print(event.stringify())
        await event.reply("Hey!")

    client.run_until_disconnected()
