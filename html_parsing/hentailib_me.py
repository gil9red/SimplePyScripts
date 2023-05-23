#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import re

import requests


def get_images(url: str) -> list[str]:
    rs = requests.get(url)

    info = re.search("window.__info = (.+?);", rs.text)
    if not info:
        print("[#] Not found window.__info!")
        return []

    pages = re.search("window.__pg = (.+?);", rs.text)
    if not pages:
        print("[#] Not found window.__pg!")
        return []

    info = json.loads(info.group(1))
    pages = json.loads(pages.group(1))

    url_chapter = info["img"]["url"]
    url_base = info["servers"]["main"] + url_chapter

    return [url_base + p["u"] for p in pages]


if __name__ == "__main__":
    url = "https://hentailib.me/koshkodevochki-eto-lozh/v1/c1?page=1"
    items = get_images(url)

    print(f"Images ({len(items)}):")
    for i, url in enumerate(items, 1):
        print(f"    {i}. {url}")

    # Images (22):
    #     1. https://img2.hentailib.me/manga/koshkodevochki-eto-lozh/chapters/468545/02_iips.png
    #     2. https://img2.hentailib.me/manga/koshkodevochki-eto-lozh/chapters/468545/03_67pz.png
    #     3. https://img2.hentailib.me/manga/koshkodevochki-eto-lozh/chapters/468545/04_v5SN.png
    #     4. https://img2.hentailib.me/manga/koshkodevochki-eto-lozh/chapters/468545/05_0dsy.png
    #     5. https://img2.hentailib.me/manga/koshkodevochki-eto-lozh/chapters/468545/06_guTg.png
    #     6. https://img2.hentailib.me/manga/koshkodevochki-eto-lozh/chapters/468545/07_cCtQ.png
    #     7. https://img2.hentailib.me/manga/koshkodevochki-eto-lozh/chapters/468545/08_EQUb.png
    #     8. https://img2.hentailib.me/manga/koshkodevochki-eto-lozh/chapters/468545/09_UfrK.png
    #     9. https://img2.hentailib.me/manga/koshkodevochki-eto-lozh/chapters/468545/10_bffa.png
    #     10. https://img2.hentailib.me/manga/koshkodevochki-eto-lozh/chapters/468545/11_7iDq.png
    #     11. https://img2.hentailib.me/manga/koshkodevochki-eto-lozh/chapters/468545/12_bwHN.png
    #     12. https://img2.hentailib.me/manga/koshkodevochki-eto-lozh/chapters/468545/13_ENhV.png
    #     13. https://img2.hentailib.me/manga/koshkodevochki-eto-lozh/chapters/468545/14_wisV.png
    #     14. https://img2.hentailib.me/manga/koshkodevochki-eto-lozh/chapters/468545/15_uVKc.png
    #     15. https://img2.hentailib.me/manga/koshkodevochki-eto-lozh/chapters/468545/16_DOEE.png
    #     16. https://img2.hentailib.me/manga/koshkodevochki-eto-lozh/chapters/468545/17_D3O1.png
    #     17. https://img2.hentailib.me/manga/koshkodevochki-eto-lozh/chapters/468545/18_Y8S2.png
    #     18. https://img2.hentailib.me/manga/koshkodevochki-eto-lozh/chapters/468545/19_g7SA.png
    #     19. https://img2.hentailib.me/manga/koshkodevochki-eto-lozh/chapters/468545/20_B9qA.png
    #     20. https://img2.hentailib.me/manga/koshkodevochki-eto-lozh/chapters/468545/21_IhKI.png
    #     21. https://img2.hentailib.me/manga/koshkodevochki-eto-lozh/chapters/468545/22_sUOK.png
    #     22. https://img2.hentailib.me/manga/koshkodevochki-eto-lozh/chapters/468545/23_PY78.png
