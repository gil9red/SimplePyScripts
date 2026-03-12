#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
import sqlite3

from pathlib import Path
from typing import Any

from root_config import JIRA_HOST
from root_common import session


DIR: Path = Path(__file__).resolve().parent
FILE_NAME_DB: Path = DIR / "jira_local.sqlite"

URL_SEARCH = f"{JIRA_HOST}/rest/api/latest/search"


def init_sqlite(filename: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(filename)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS Task (
            id INTEGER PRIMARY KEY,
            key TEXT,
            summary TEXT,
            description TEXT,
            status TEXT,
            issue_type TEXT,
            created TEXT,
            is_indexed INTEGER DEFAULT 0
        )
    """
    )
    conn.commit()
    return conn


def get_last_id(conn: sqlite3.Connection, project: str) -> int:
    res = conn.execute(
        "SELECT MAX(id) FROM Task WHERE key LIKE ?", (f"{project}-%",)
    ).fetchone()
    return res[0] if res[0] else 0


def sync_jira_to_sqlite(conn: sqlite3.Connection, projects: list[str]):
    max_results: int = 100

    for project in projects:
        last_id: int = get_last_id(conn, project)

        while True:
            print(f"[*] Поиск задач в Jira проекта {projects} от ID > {last_id}...")

            filter_id: str = f"AND id > {last_id}" if last_id > 0 else ""
            jql: str = f"project = {project} {filter_id} ORDER BY id ASC"

            query: dict[str, Any] = {
                "jql": jql,
                "fields": "key,summary,description,status,issuetype,created",
                "maxResults": max_results,
            }

            rs = session.get(URL_SEARCH, params=query)
            try:
                rs.raise_for_status()
            except Exception as e:
                print(rs.json())
                raise e

            issues: list[dict] = rs.json().get("issues")
            if not issues:
                print("Больше нет задач")
                break

            for issue in issues:
                print(issue)

                issue_id: int = int(issue["id"])
                issue_key: str = issue["key"]
                issue_summary: str = issue["fields"].get("summary", "")
                issue_desc: str = str(issue["fields"].get("description"))
                issue_status: str = issue["fields"]["status"]["name"]
                issue_type: str = issue["fields"]["issuetype"]["name"]
                issue_created: str = issue["fields"]["created"]

                conn.execute(
                    """
                        INSERT OR IGNORE INTO Task 
                        (id, key, summary, description, status, issue_type, created)
                        VALUES
                        (?, ?, ?, ?, ?, ?, ?)
                        """,
                    (
                        issue_id,
                        issue_key,
                        issue_summary,
                        issue_desc,
                        issue_status,
                        issue_type,
                        issue_created,
                    ),
                )

                last_id = issue_id

            conn.commit()

            print(f"[+] Загружено {len(issues)} задач...")

            time.sleep(5)


if __name__ == "__main__":
    # TODO: Возможность задавать аргументом
    projects: list[str] = [
        # "OPTT",
        "TXI",
        "TWRBS",
        "TXCORE",
        "TXACQ",
    ]

    # TODO: Возможность задавать аргументом путь к БД
    # FILE_NAME_DB: Path = DIR / "jira_local_OPTT.sqlite"

    db_conn = init_sqlite(FILE_NAME_DB)
    sync_jira_to_sqlite(db_conn, projects)
