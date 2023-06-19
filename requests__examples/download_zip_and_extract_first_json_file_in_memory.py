#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import io
import zipfile

import requests


rs = requests.get("https://op.mos.ru/EHDWSREST/catalog/export/get?id=84505")
zip_data = io.BytesIO(rs.content)

with zipfile.ZipFile(zip_data) as zip_file:
    json_file_name = zip_file.namelist()[0]
    print(json_file_name)

    json_data = zip_file.read(json_file_name)
    json_data = json_data.decode("cp1251")
    print(json_data[:50])

    obj = json.loads(json_data)
    print(obj[0]["AdmArea"])
