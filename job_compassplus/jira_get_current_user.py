#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from typing import Any

from root_config import JIRA_HOST
from root_common import session


URL_API_MYSELF = f"{JIRA_HOST}/rest/api/latest/myself"


def get_current_user() -> dict[str, Any]:
    rs = session.get(URL_API_MYSELF)
    rs.raise_for_status()

    return rs.json()


if __name__ == "__main__":
    user = get_current_user()
    print("Current user:", user)
    print("Current user name:", user["name"])
    print()

    import json
    print(f"Current user (pretty):\n{json.dumps(user, indent=4)}")
