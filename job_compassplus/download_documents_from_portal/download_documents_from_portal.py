#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import time

from pathlib import Path
from urllib.parse import quote

# TODO: Мб файл проекта добавить? Хотя бы pip install
import openpyxl
from requests.exceptions import HTTPError

DIR: Path = Path(__file__).parent
ROOT_DIR: Path = DIR.parent

sys.path.append(str(ROOT_DIR))
from site_common import do_get

DIR_DOWNLOADS: Path = DIR / "downloads"

# TODO: Из аргументов
path_excel: Path = Path(r"C:\DOC\Visa\documents-2026.xlsx")

path_downloads: Path = DIR_DOWNLOADS / path_excel.name
path_downloads.mkdir(parents=True, exist_ok=True)

workbook = openpyxl.load_workbook(path_excel, data_only=True)
# sheet = workbook["query(1)"]  # TODO: Из аргументов, по умолчанию первый
sheet = workbook.worksheets[0]

for (cell_name, *_) in sheet.iter_rows(min_row=2, values_only=False):
    file_name: str = cell_name.value

    file_url: str = cell_name.hyperlink.target
    if cell_name.hyperlink.location:  # NOTE: В документе была # в ссылке
        file_url = f"{file_url}%23{cell_name.hyperlink.location}"

    # TODO: Проверить, режим force, чтобы не проверять наличие файла - из аргументов
    path_download_file: Path = path_downloads / file_name
    if path_download_file.exists():
        print(f"{file_name!r} already exists, skipping")
        continue

    print(f"Downloading {file_name!r} from {file_url}")

    # TODO: Настройка пропуска файлов, при ошибке 404?
    # TODO: Или попробовать по имени файла загрузить?
    try:
        rs = do_get(file_url)
        print(rs)
    except HTTPError as e:
        if e.response.status_code != 404:
            raise e

        new_file_url: str = file_url.rsplit("/", maxsplit=1)[0] + f"/{quote(file_name)}"
        print(f"[#] Error 404 for {file_url!r}, trying new url: {new_file_url!r}")

        rs = do_get(new_file_url)
        print(rs)

    print(f"Saving file to: {path_download_file}")
    path_download_file.write_bytes(rs.content)

    time.sleep(1)

workbook.close()
