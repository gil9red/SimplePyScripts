#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/LonamiWebs/Telethon
# SOURCE: https://my.telegram.org/apps


# pip install telethon
from telethon.sync import TelegramClient

from config import API_ID, API_HASH


with TelegramClient("my", API_ID, API_HASH) as client:
    for i, dialog in enumerate(client.iter_dialogs(), 1):
        print(f"{i:3}. {dialog.name!r}")
