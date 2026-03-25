#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Self

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(ROOT_DIR))
from root_config import JIRA_HOST
from root_common import session


# Examples:
"""
{
    "system": [
        {"id":"10122","isSystemAvatar":true,"isSelected":false,"isDeletable":false,"urls":{"48x48":"https://.../useravatar?avatarId=10122","24x24":"https://.../useravatar?size=small&avatarId=10122","16x16":"https://.../useravatar?size=xsmall&avatarId=10122","32x32":"https://.../useravatar?size=medium&avatarId=10122"},"selected":false},
        ...
        {"id":"17241","isSystemAvatar":true,"isSelected":true,"isDeletable":false,"urls":{"48x48":"https://.../useravatar?avatarId=17241","24x24":"https://.../useravatar?size=small&avatarId=17241","16x16":"https://.../useravatar?size=xsmall&avatarId=17241","32x32":"https://.../useravatar?size=medium&avatarId=17241"},"selected":true},
        ...
        {"id":"17252","isSystemAvatar":true,"isSelected":false,"isDeletable":false,"urls":{"48x48":"https://.../useravatar?avatarId=17252","24x24":"https://.../useravatar?size=small&avatarId=17252","16x16":"https://.../useravatar?size=xsmall&avatarId=17252","32x32":"https://.../useravatar?size=medium&avatarId=17252"},"selected":false}],
    "custom": []
}
"""


@dataclass(frozen=True)
class AvatarUrls:
    size_48x48: str
    size_32x32: str
    size_24x24: str
    size_16x16: str

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> Self:
        return cls(
            size_48x48=data.get("48x48"),
            size_24x24=data.get("24x24"),
            size_32x32=data.get("32x32"),
            size_16x16=data.get("16x16"),
        )


@dataclass(frozen=True)
class JiraAvatar:
    id: str
    is_system_avatar: bool
    is_selected: bool
    is_deletable: bool
    urls: AvatarUrls
    selected: bool  # NOTE: Дублирует isSelected

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            id=data["id"],
            is_system_avatar=data["isSystemAvatar"],
            is_selected=data["isSelected"],
            is_deletable=data["isDeletable"],
            urls=AvatarUrls.from_dict(data["urls"]),
            selected=data["selected"],
        )


@dataclass(frozen=True)
class JiraAvatarResponse:
    system: list[JiraAvatar]
    custom: list[JiraAvatar]

    @classmethod
    def from_dict(cls, data: dict[str, list[dict[str, Any]]]) -> Self:
        def _get_avatars(key: str) -> list[JiraAvatar]:
            return [JiraAvatar.from_dict(d) for d in data[key]]

        return cls(
            system=_get_avatars("system"),
            custom=_get_avatars("custom"),
        )


def get_avatars(username: str) -> JiraAvatarResponse:
    url = f"{JIRA_HOST}/rest/api/latest/user/avatars?username={username}"

    rs = session.get(url)
    rs.raise_for_status()

    return JiraAvatarResponse.from_dict(rs.json())


if __name__ == "__main__":
    rs: JiraAvatarResponse = get_avatars("ipetrash")

    print(f"System ({len(rs.system)}):")
    for i, avatar in enumerate(rs.system, 1):
        print(f"    {i}. {avatar}")

    print()

    print(f"Custom ({len(rs.custom)}):")
    for i, avatar in enumerate(rs.custom, 1):
        print(f"    {i}. {avatar}")
