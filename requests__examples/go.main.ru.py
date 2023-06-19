#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import re
import sys

import requests


rs = requests.get("https://go.mail.ru/search?q=cats")
print(rs)

data = re.search("go.dataJson = (.+);", rs.text)
if not data:
    print("Not data!")
    sys.exit()

data = data.group(1)

rs_data = json.loads(data)
print(rs_data)

for result in rs_data["serp"]["results"]:
    if "url" not in result:
        continue

    print(result["url"])

# http://mau.ru/
# https://ru.wikipedia.org/wiki/%D0%9A%D0%BE%D1%88%D0%BA%D0%B8_(%D0%BC%D1%8E%D0%B7%D0%B8%D0%BA%D0%BB)
# http://cats-crasharena.ru/
# http://vk.com/vk.cats
# https://trashbox.ru/link/zeptolab-cats-android
# https://wooordhunt.ru/word/cats
# https://play.google.com/store/apps/details?hl=ru&id=com.zeptolab.cats.google
# http://www.youtube.com/channel/UC4uhxfDlhySxeEQldGsn4TQ
# http://anolink.ru/category/igry/battle-cats/
# https://www.babla.ru/%D0%B0%D0%BD%D0%B3%D0%BB%D0%B8%D0%B9%D1%81%D0%BA%D0%B8%D0%B9-%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9/cats
