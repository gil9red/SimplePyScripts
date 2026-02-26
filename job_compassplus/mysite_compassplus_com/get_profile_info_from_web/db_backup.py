#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sqlite3
import traceback
import time
import zipfile

from datetime import date
from pathlib import Path

from config import DIR_DB_BACKUP
from db import db


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/b144a9c8fa6e737ef177fe1f7ae07d61794fc037/sqlite3__examples/backup__examples/common.py#L15
def create_zip_for_file(
    file_name_zip: str | Path,
    file_name: Path,
    delete_file_name: bool = True,
):
    with zipfile.ZipFile(
        file_name_zip, mode="w", compression=zipfile.ZIP_DEFLATED
    ) as f:
        f.write(file_name, arcname=file_name.name)

    if delete_file_name:
        file_name.unlink()


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/bfac99ef66038562f16c94341535e0ce02f1dec2/sqlite3__examples/backup__examples/backup_via_api.py#L17
def backup(
    connect: sqlite3.Connection,
    file_name: Path,
    use_zip: bool = True,
    delete_file_name_after_zip: bool = True,
) -> Path:
    dst = sqlite3.connect(file_name)
    connect.backup(dst)
    dst.close()

    if use_zip:
        file_name_zip = Path(f"{file_name}.zip")
        create_zip_for_file(
            file_name_zip, file_name, delete_file_name=delete_file_name_after_zip
        )
        return file_name_zip

    return file_name


def do_backup_db() -> None:
    prefix: str = "[do_backup_db]"

    print(f"{prefix} Start")

    while True:
        print(f"{prefix} Check")
        try:
            file_name_backup = backup(
                connect=db.connection(),
                file_name=DIR_DB_BACKUP / f"{date.today().isoformat()}.sqlite",
            )
            print(f"{prefix} Backup saved to {file_name_backup}")

        except Exception:
            # Выводим ошибку в консоль
            tb = traceback.format_exc()
            print(f"{prefix} Error:\n{tb}")

        finally:
            time.sleep(30 * 24 * 60 * 60)  # Раз в 30 дней


if __name__ == "__main__":
    do_backup_db()
