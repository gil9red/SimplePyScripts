#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install python-telegram-bot
from telegram import InlineKeyboardMarkup

# pip install python-telegram-bot-pagination
from telegram_bot_pagination import InlineKeyboardPaginator


def is_equal_inline_keyboards(
    keyboard_1: InlineKeyboardPaginator, keyboard_2: InlineKeyboardMarkup
) -> bool:
    keyboard_1 = keyboard_1.keyboard
    keyboard_1_data = [x["text"] for x in keyboard_1]

    keyboard_2 = keyboard_2.to_dict()["inline_keyboard"][0]
    keyboard_2_data = [x["text"] for x in keyboard_2]

    return keyboard_1_data == keyboard_2_data
