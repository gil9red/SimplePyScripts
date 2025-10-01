#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
import time

from pathlib import Path
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from common import session


def get_valid_filename(s: str) -> str:
    s = s.strip().replace(":", ".")
    return re.sub(r"(?u)[^-\w. ]", "", s)


DIR = Path(__file__).resolve().parent


def parse(start_url: str, download_path: Path = DIR):
    url = start_url

    while True:
        rs = session.get(url)
        soup = BeautifulSoup(rs.content, "html.parser")

        title: str = soup.select_one("title").get_text(strip=True)
        print(title)

        img_urls: list[str] = []
        for img_el in soup.select("img[data-media-id]"):
            media_id = img_el["data-media-id"]
            url = urljoin(rs.url, f"/api/media/{media_id}")
            if url not in img_urls:
                img_urls.append(url)

        if img_urls:
            print(f"    Изображений: {len(img_urls)}")

            # Example: 'Да будет благословен этот прекрасный мир! / Том 666 / Веб-новелла: Короткая история богини'
            #       -> ['Да будет благословен этот прекрасный мир', 'Том 666', 'Веб-новелла Короткая история богини']
            parts: list[str] = [get_valid_filename(el) for el in title.split("/")]
            ranobe_title: str = parts[0]
            chapter_title: str = ". ".join(parts[1:])

            dir_ranobe: Path = download_path / ranobe_title
            dir_ranobe.mkdir(parents=True, exist_ok=True)

            for i, url in enumerate(img_urls, 1):
                rs = session.get(url)
                time.sleep(0.1)

                img_path: Path = dir_ranobe / f"{chapter_title}. {i}.png"
                img_path.write_bytes(rs.content)

        next_chapter_link_el = soup.select_one("a[data-next-chapter-link]")
        if not next_chapter_link_el.get("href"):
            break

        url: str = urljoin(rs.url, next_chapter_link_el["href"])

        time.sleep(1)


if __name__ == "__main__":
    url = "https://ranobehub.org/ranobe/131/1/1"
    parse(url)
