#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import re
from urllib.parse import urljoin
from urllib.request import urlretrieve

import requests
from bs4 import BeautifulSoup

from config import GIST_URL, DIR_GIST_FILES


# Clear directory
for file_name in DIR_GIST_FILES.glob('*'):
    file_name.unlink()


rs = requests.get(GIST_URL)
root = BeautifulSoup(rs.content, 'html.parser')

for a in root.find_all("a", {"href": re.compile(r'/raw/.+/group\d+')}):
    url = urljoin(rs.url, a['href'])
    file_name = re.search(r'/(group\d+)', url).group(1)

    print(url)
    urlretrieve(url, DIR_GIST_FILES / file_name)
