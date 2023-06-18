#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install emoji
import emoji


text = "😌😌😌🤤😋😇😝🤑😍😚😙😐🤓😴😌🤗🙂😁🤑🤥😔🥺🤯💩😹😸👨‍🦰👨‍🦲👩‍❤‍💋‍👨👐🏻🖖🏻✋🏻🦵🏻Какой прекрасный день!"
new_text = "".join(char for char in text if char not in emoji.UNICODE_EMOJI)

print(new_text)
# ‍‍‍‍‍Какой прекрасный день!
