#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import random

from common import (
    session,
    get_comics_image_url,
    get_last_commics_id,
    get_comics_url_by_id,
    get_comics_info,
)


def get_random_comics_url() -> str:
    comics_number = get_last_commics_id()

    random_comics_number = random.randint(1, comics_number)
    return get_comics_url_by_id(random_comics_number)


def get_random_comics_image_url() -> str:
    url = get_random_comics_url()

    return get_comics_image_url(url)


def get_random_comics_info() -> tuple[str, str, str]:
    url = get_random_comics_url()

    return get_comics_info(url)


if __name__ == "__main__":
    url_comics = get_random_comics_url()
    print("url_comics:", url_comics)

    url_image = get_comics_image_url(url_comics)
    print("url_image:", url_image)

    comics_id = url_comics.split("/")[-2]

    from pathlib import Path

    current_dir: Path = Path(__file__).resolve().parent
    downloads_dir: Path = current_dir / "downloads"
    downloads_dir.mkdir(parents=True, exist_ok=True)

    file_name = downloads_dir / f"{comics_id}.jpg"
    print(f"Saving to: {file_name}")

    # TODO: Повторяет логику из download_all.py
    with open(file_name, mode="wb") as f:
        rs = session.get(url_image)
        rs.raise_for_status()

        f.write(rs.content)

    print()
    print("Random comics image:")
    print(get_random_comics_image_url())
    print(get_random_comics_image_url())
    print(get_random_comics_image_url())

    print()
    print("Random comics image:")
    print(get_random_comics_info())
    print(get_random_comics_info())
    print(get_random_comics_info())
