#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/s0md3v/Photon/wiki/Photon-Library


import json

# pip install photon
import photon


photon.crawl("https://github.com/s0md3v/Photon/wiki/Photon-Library")
result = photon.result()
print(result)

with open("result.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=4, ensure_ascii=False)
