#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import re

import requests


rs = requests.get("https://magnit.ru/shops/")
m = re.search("var elementsArr = (.+);", rs.text)

data = json.loads(m.group(1))
# {'points': [{'id': 49215, 'city': '2398', 'lat': '55.742145', 'lng': '37.520419', 'address': ...

points = data["points"]

print(f"Points ({len(points)}):")
for p in points:
    print(f"  lat: {p['lat']}, lng: {p['lng']}")

# Points (617):
#   lat: 55.742145, lng: 37.520419
#   lat: 55.741764, lng: 37.520348
#   lat: 55.741757, lng: 37.520355
#   ...
#   lat: 55.877706, lng: 37.731395
#   lat: 55.876482, lng: 37.721799
#   lat: 55.878682, lng: 37.719253
