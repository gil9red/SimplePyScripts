#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path
from peewee import SqliteDatabase


def backup(db: SqliteDatabase, file_name: Path | str) -> None:
    Path(file_name).unlink(missing_ok=True)

    db.connection().execute("VACUUM INTO ?", (str(file_name),))


if __name__ == "__main__":
    from common import run_test

    run_test(
        backup=backup,
        file_name_backup=Path(__file__).resolve().name + ".db",
    )
