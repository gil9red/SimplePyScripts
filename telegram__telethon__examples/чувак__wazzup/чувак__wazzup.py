#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/LonamiWebs/Telethon
# SOURCE: https://my.telegram.org/apps


import random
import sys

from glob import glob

# pip install telethon
from telethon.sync import TelegramClient, events

sys.path.append("..")
from config import API_ID, API_HASH


IMAGES = glob("images/*.jpg")


with TelegramClient("../my", API_ID, API_HASH) as client:
    me_id = client.get_me().id

    @client.on(events.NewMessage(pattern="(?i).*чу+ва+к|wa+zz+u+p"))
    async def handler(event):
        print(event.stringify())

        if event.chat_id == me_id or event.message.from_id == me_id:
            return

        chat = await event.get_chat()

        await client.send_file(
            chat,
            random.choice(IMAGES),
            reply_to=event.message.id,
        )

    client.run_until_disconnected()
