#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as DT
import json
import re
import sys

from bs4 import BeautifulSoup
import requests


JS_SHARED_DATA_PATTERN = re.compile("window._sharedData = ({.+});")


# SOURCE: https://ru.stackoverflow.com/q/1153084/201445
url = "https://www.instagram.com/p/B5n2EXjF_1C/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
}


rs = requests.get(url, headers=headers)
root = BeautifulSoup(rs.content, "html.parser")

script_el = root.find(
    "script", attrs={"type": "text/javascript"}, text=JS_SHARED_DATA_PATTERN
)
print(script_el)
# <script type="text/javascript">window._sharedData = {"config":{"csrf_tok ...

print(script_el.text)
# window._sharedData = {"config":{"csrf_token":"RtSXgxK6b0Lh4Ag3 ...

m = JS_SHARED_DATA_PATTERN.search(script_el.text)
if not m:
    file_name_dump = str(DT.datetime.now()).replace(":", "") + ".html"
    with open(file_name_dump, "wb") as f:
        f.write(rs.content)
    print(f'Not found "window._sharedData = ", see: {file_name_dump}!')
    sys.exit()

shared_data_text = m.group(1)
print(shared_data_text)
# {"config":{"csrf_token":"RtSXgxK6b0Lh4Ag3wSFReb ...

data = json.loads(shared_data_text)
print(data)
# {'config': {'csrf_token': 'RtSXgxK6b0Lh4Ag3wSFReb ...
