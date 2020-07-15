#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import requests
import json
from bs4 import BeautifulSoup
import re


JS_SHARED_DATA_PATTERN = re.compile('window._sharedData = ({.+});')


# SOURCE: https://ru.stackoverflow.com/q/1153084/201445
url = 'https://www.instagram.com/p/B5n2EXjF_1C/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}


rs = requests.get(url, headers=headers)
root = BeautifulSoup(rs.content, 'html.parser')

script_el = root.find('script', attrs={'type': "text/javascript"}, text=JS_SHARED_DATA_PATTERN)
print(script_el)
# <script type="text/javascript">window._sharedData = {"config":{"csrf_tok ...

print(script_el.text)
# window._sharedData = {"config":{"csrf_token":"RtSXgxK6b0Lh4Ag3 ...

shared_data_text = JS_SHARED_DATA_PATTERN.search(script_el.text).group(1)
print(shared_data_text)
# {"config":{"csrf_token":"RtSXgxK6b0Lh4Ag3wSFReb ...

data = json.loads(shared_data_text)
print(data)
# {'config': {'csrf_token': 'RtSXgxK6b0Lh4Ag3wSFReb ...
