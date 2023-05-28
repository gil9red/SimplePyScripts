#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json


def dict_clean(items, default):
    return {k: default if v is None else v for k, v in items}


text = """
{
    "Action-bar": null,
    "Action": "Action",
    "Children": [
        {"Action": null},
        {"Action": true},
        {"Action": "false"},
        {"Action": {"need": null}}
    ],
    "RGB-bar": null
}
"""


genre_translate = json.loads(
    text,
    encoding="utf-8",
    object_pairs_hook=lambda items: dict_clean(items, default=[]),
)
print(genre_translate)
# {'Action-bar': [], 'Action': 'Action', 'Children': [{'Action': []}, {'Action': True}, {'Action': 'false'}, {'Action': {'need': []}}], 'RGB-bar': []}

genre_translate = json.loads(
    text,
    encoding="utf-8",
    object_pairs_hook=lambda items: dict_clean(items, default="<null>"),
)
print(genre_translate)
# {'Action-bar': '<null>', 'Action': 'Action', 'Children': [{'Action': '<null>'}, {'Action': True}, {'Action': 'false'}, {'Action': {'need': '<null>'}}], 'RGB-bar': '<null>'}
