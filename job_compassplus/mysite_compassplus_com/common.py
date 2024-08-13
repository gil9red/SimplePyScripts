#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
from pathlib import Path
from typing import Any

from bs4 import Tag

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(ROOT_DIR))
from site_common import do_get, do_post


URL_BASE = "https://mysite.compassplus.com"
URL = f"{URL_BASE}/Person.aspx?accountname={{}}"


def get_profile_organization(full_username: str) -> dict[str, Any]:
    url = f"{URL_BASE}/_vti_bin/SilverlightProfileService.json/GetUserSLProfileData"
    rs = do_post(url, json={"AccountNames": [full_username]})
    return rs.json()


def is_active_profile(full_username: str) -> bool:
    organization = get_profile_organization(full_username)
    data = organization["d"][0]
    # Если хотя бы один из них имеет значение, отличное от [] или None
    return bool(data["Parent"] or data["Siblings"] or data["Children"])


def get_text(el: Tag) -> str:
    return el.get_text(strip=True)


if __name__ == "__main__":
    full_username = r"CP\ipetrash"

    rs = do_get(URL.format(full_username))
    print(rs)

    organization = get_profile_organization(full_username)
    print(organization)

    data = organization["d"][0]
    print("Parent:", data["Parent"])
    print("Siblings:", data["Siblings"])
    print("Children:", data["Children"])
    print()

    print("Is active:", is_active_profile(full_username))
