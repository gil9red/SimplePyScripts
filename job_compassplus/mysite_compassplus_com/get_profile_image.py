#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from urllib.parse import urljoin
from bs4 import BeautifulSoup
from common import session, URL


def get_profile_image(username: str, domain: str = "CP") -> bytes | None:
    url = URL.format(fr"{domain}\{username}")

    rs = session.get(url)
    rs.raise_for_status()

    root = BeautifulSoup(rs.content, "html.parser")
    img_el = root.select_one("#ctl00_PictureUrlImage")
    if not img_el:  # Сайт не умеет показывать 404 при отсутствующем пользователе
        return

    img_url = urljoin(rs.url, img_el["src"])

    rs = session.get(img_url)
    rs.raise_for_status()

    return rs.content


if __name__ == "__main__":
    username = "ipetrash"

    img_data = get_profile_image(username)
    print(len(img_data), img_data[:20])

    from pathlib import Path
    img_path = Path(__file__).parent / f"{username}.jpg"
    img_path.write_bytes(img_data)
