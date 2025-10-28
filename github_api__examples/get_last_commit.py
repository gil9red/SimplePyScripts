#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

import requests


@dataclass
class CommitUser:
    name: str
    email: str
    date: datetime

    @classmethod
    def parse_from_dict(cls, data: dict[str, Any]) -> "CommitUser":
        return cls(
            name=data["name"],
            email=data["email"],
            date=datetime.fromisoformat(data["date"]),
        )


# TODO: Поддержка всех полей
@dataclass
class Commit:
    sha: str
    message: str
    author: CommitUser
    committer: CommitUser

    @classmethod
    def parse_from_dict(cls, data: dict[str, Any]) -> "Commit":
        return cls(
            sha=data["sha"],
            message=data["commit"]["message"],
            author=CommitUser.parse_from_dict(data["commit"]["author"]),
            committer=CommitUser.parse_from_dict(data["commit"]["committer"]),
        )


def get_last_commit(owner: str, repository: str) -> Commit:
    url: str = f"https://api.github.com/repos/{owner}/{repository}/commits?per_page=1"

    rs = requests.get(url)
    rs.raise_for_status()

    result: dict[str, Any] = rs.json()[0]
    return Commit.parse_from_dict(result)


if __name__ == '__main__':
    commit = get_last_commit(owner="gil9red", repository="RPG-Maker-MZ-Foo")
    print(commit)
    # Commit(sha='816a821788e113fdc80d17190fa1ed743c4b1524', message='Обновление. Улучшение алгоритма шагающей леди', author=CommitUser(name='gil9red', email='ilya.petrash@inbox.ru', date=datetime.datetime(2025, 10, 25, 18, 53, 41, tzinfo=datetime.timezone.utc)), committer=CommitUser(name='gil9red', email='ilya.petrash@inbox.ru', date=datetime.datetime(2025, 10, 25, 18, 53, 41, tzinfo=datetime.timezone.utc)))

    print(datetime.now(UTC) - commit.author.date)
    # 2 days, 14:21:39.576065
