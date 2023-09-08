#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
import subprocess
import xml.etree.ElementTree as ET

from datetime import date, timedelta

from get_last_release_version import get_last_release_version


PATTERN_RELEASE_VERSION = re.compile(r"Release version ([\d.]+) ")

URL_DEFAULT_SVN_PATH = "svn+cplus://svn2.compassplus.ru/twrbs/trunk/dev"


def find_release_version(
    text: str,
    version: str,
    last_days: int = 30,
    url_svn_path: str = URL_DEFAULT_SVN_PATH,
) -> str:
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
        last_revision = logentry_el.attrib["revision"]
        break

    if not last_revision:
        raise Exception("Не удалось найти ревизию!")

    last_release_version: str = get_last_release_version(
        version=version,
        start_revision=last_revision,
        last_days=last_days,
        url_svn_path=url_svn_path,
    )

    # Первый коммит, который искали попал уже в следующую версию, поэтому
    # нужно добавить 1 к последней версии:
    #     3.2.35.10.10 -> 3.2.35.10.11
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
