#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sqlite3
from config import TOKEN


def create_connect():
    return sqlite3.connect("gist_commits.sqlite")


def init_db() -> None:
    # Создание базы и таблицы
    with create_connect() as connect:
        connect.execute(
            """
            CREATE TABLE IF NOT EXISTS GistFile (
                id INTEGER PRIMARY KEY,
                commit_hash TEXT NOT NULL,
                committed_at DATETIME NOT NULL,
                raw_url TEXT NOT NULL,
                content CLOB NOT NULL,
                
                CONSTRAINT raw_url_unique UNIQUE (commit_hash, raw_url)
            );
        """
        )

        connect.commit()


if __name__ == "__main__":
    import traceback

    # pip install pygithub
    from github import Github

    init_db()

    gh = Github(TOKEN)
    # #
    # # OR:
    # # But: "github.GithubException.RateLimitExceededException: 403 {'message': "API rate limit exceeded for \
    # # 79.000.10.000. (But here's the good news: Authenticated requests get a higher rate limit. Check out the
    # # documentation for more details.)", 'documentation_url': 'https://developer.github.com/v3/#rate-limiting'}"
    # gh = Github()

    gist = gh.get_gist("2f80a34fb601cd685353")
    print(gist)
    print(f"History ({len(gist.history)}):")

    with create_connect() as connect:
        try:
            for history in reversed(gist.history):
                print(
                    f"  committed_at: {history.committed_at}, version: {history.version}, files: {history.files}"
                )

                if "gistfile1.txt" not in history.files:
                    print('  Not found file "gistfile1.txt"!')
                    continue

                file = history.files["gistfile1.txt"]
                # print('    url: {}'.format(file.raw_url))
                # print('    [{}]: {}'.format(len(file.content), repr(file.content)[:150]))
                # print()

                connect.execute(
                    "INSERT OR IGNORE INTO GistFile (commit_hash, committed_at, raw_url, content) VALUES (?, ?, ?, ?)",
                    (history.version, history.committed_at, file.raw_url, file.content),
                )

        except Exception as e:
            print(f"ERROR: {e}:\n\n{traceback.format_exc()}")
