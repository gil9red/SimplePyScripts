#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


rs = requests.get("https://www.flickr.com/search/?text=cats")
root = BeautifulSoup(rs.content, "html.parser")

for x in root.select(".view.photo-list-photo-view[style]"):
    m = re.search(r"url\((.+?)\)", x["style"])
    url_img = urljoin(rs.url, m.group(1))
    print(url_img)

"""
https://live.staticflickr.com/5598/14934282524_344c84246b_n.jpg
https://live.staticflickr.com/4838/45925416992_c9caac8cb9_m.jpg
https://live.staticflickr.com/4536/38465451442_59291a4a2f_n.jpg
...
https://live.staticflickr.com/70/175237265_029f7974a2_w.jpg
https://live.staticflickr.com/3488/4051998735_5b4863ac11_m.jpg
https://live.staticflickr.com/5036/5881933297_7974eaff82_n.jpg
"""
