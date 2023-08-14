#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path

from common import session, BASE_URL
from collect_wishes import Wish


DIR = Path(__file__).resolve().parent
DIR_IMAGES = DIR / "images"

DIR_IMAGES.mkdir(parents=True, exist_ok=True)


wish = Wish.select().where(Wish.img_url != "").get()

img_url = f"{BASE_URL}{wish.img_url}"
rs = session.get(img_url)

file_name = DIR_IMAGES / f"{wish.id}.jpg"
file_name.write_bytes(rs.content)
print(f"Сохранено в {file_name}")
