#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
import re

from pathlib import Path

from common import session, get_last_commics_id, get_comics_info

CURRENT_DIR: Path = Path(__file__).resolve().parent
DOWNLOADS_DIR: Path = CURRENT_DIR / "downloads"
DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)


def download_all(downloads_dir: Path = DOWNLOADS_DIR) -> None:
    comics_number = get_last_commics_id()
    for comics_id in range(1, comics_number + 1):
        url_comics, title, url_image = get_comics_info(comics_id)
        print(f"#{comics_id}. {title!r}: {url_image}")

        clear_title: str = re.sub(r'[^\w\- ]', '', title)
        file_name: Path = downloads_dir / f"{comics_id} - {clear_title}.jpg"
        print(f"Saving to: {file_name}")

        # TODO: Повторяет логику из get_random_comics.py
        with open(file_name, mode="wb") as f:
            rs = session.get(url_image)
            rs.raise_for_status()

            f.write(rs.content)

        print()

        time.sleep(1)


if __name__ == '__main__':
    download_all()
