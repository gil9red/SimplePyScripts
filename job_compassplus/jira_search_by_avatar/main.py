#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import time
from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(ROOT_DIR))
from root_config import JIRA_HOST
from root_common import session


URL_PROFILE_FORMAT = f"{JIRA_HOST}/secure/ViewProfile.jspa?name={{name}}"
URL_USER_SEARCH = f"{JIRA_HOST}/rest/api/latest/user/search"


def search_by_avatar(avatar_id: int) -> list[dict]:
    start_at = 0
    max_results = 500

    avatar_id = str(avatar_id)

    items = []
    while True:
        params = {
            "username": ".",
            "startAt": start_at,
            "maxResults": max_results,
        }

        rs = session.get(URL_USER_SEARCH, params=params)
        rs.raise_for_status()

        result = rs.json()
        if not result:
            break

        for user in result:
            if avatar_id in user["avatarUrls"]["48x48"]:
                items.append(user)

        time.sleep(5)

        start_at += max_results

    return items


if __name__ == "__main__":
    avatar_id = 17250  # pirate
    users = search_by_avatar(avatar_id)
    print(f"Users ({len(users)}):")
    for i, user in enumerate(users, 1):
        display_name = user["displayName"]
        user_url = URL_PROFILE_FORMAT.format(name=user["key"])
        print(f"{i}. '{display_name}': {user_url}")
