#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
import subprocess
import xml.etree.ElementTree as ET

from datetime import date, timedelta


PATTERN_RELEASE_VERSION = re.compile(r"Release version ([\d.]+) ")

URL_DEFAULT_SVN_PATH = "svn+cplus://svn2.compassplus.ru/twrbs/trunk/dev"


def find_release_version(text: str, version: str, last_days: int = 30, url_svn_path: str = URL_DEFAULT_SVN_PATH) -> str:
    url = f"{url_svn_path}/{version}"

    end_date = date.today() - timedelta(days=last_days)

    data: bytes = subprocess.check_output(
        [
            "svn",
            "log",
            # "--verbose",
            "--xml",
            "--search",
            text,
            "--revision",
            # Если в паре значений первым идет большее значение, то поиск будет идти от большего к меньшему
            f"HEAD:{{{end_date}}}",
            url,
        ]
    )
    root = ET.fromstring(data)

    last_revision = None
    for logentry_el in root.findall(".//logentry"):
        last_revision = int(logentry_el.attrib["revision"])
        break

    if not last_revision:
        raise Exception("Не удалось найти ревизию!")

    text = "Release version "
    data: bytes = subprocess.check_output(
        [
            "svn",
            "log",
            # "--verbose",
            "--xml",
            "--search",
            text,
            "--revision",
            # Если в паре значений первым идет большее значение, то поиск будет идти от большего к меньшему
            f"{last_revision}:{{{end_date}}}",
            url,
        ]
    )
    root = ET.fromstring(data)

    last_release_version_msg = None
    for logentry_el in root.findall(".//logentry"):
        last_release_version_msg = logentry_el.find("msg").text
        break

    if not last_release_version_msg:
        raise Exception("Не удалось найти коммит релиза!")

    m = PATTERN_RELEASE_VERSION.search(last_release_version_msg)
    if not m:
        raise Exception(f"Не удалось вытащить версию релиза из {last_release_version_msg!r}")

    last_release_version: str = m.group(1)

    # Первый коммит, который искали попал уже в следующую версию, поэтому
    # нужно добавить 1 к последней версии
    last_release_version = re.sub(
        r"\.(\d+)$",  # Последнее число в версии
        lambda m: f".{int(m.group(1)) + 1}",  # Увеличение числа на 1
        last_release_version
    )

    return last_release_version


if __name__ == '__main__':
    text = "TXI-8197"
    print(find_release_version(text=text, version="3.2.35.10"))
    # 3.2.35.10.11

    print(find_release_version(text=text, version="3.2.34.10"))
    # 3.2.34.10.18
