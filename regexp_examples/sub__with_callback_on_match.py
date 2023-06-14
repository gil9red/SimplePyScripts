#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re


text = """\
<item id="111">
<title>Заголовок</title>
<description>Описание</description>
<images>
<image id="111">фото1</image>
<image id="111">фото2</image>
</images>
</item>
<item id="111">
<title>Заголовок</title>
<description>Описание</description>
<images>
<image id="111">фото1</image>
<image id="111">фото2</image>
</images>
</item>
<item id="111">
<title>Заголовок</title>
<description>Описание</description>
<images>
<image id="111">фото1</image>
<image id="111">фото2</image>
</images>
</item>
"""

counter = 3000 - 1


def on_sub(_):
    global counter
    counter += 1

    return 'id="{}"'.format(counter)


new_text = re.sub(r'id="\d+"', on_sub, text)
print(new_text)
