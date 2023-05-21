#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path
from urllib.request import urlretrieve

from pathvalidate import sanitize_filename

from get_certificates import get_certificates


DIR = Path(__file__).resolve().parent

DIR_CERTS = DIR / "certs"
DIR_CERTS.mkdir(parents=True, exist_ok=True)

USER = 1381287  # https://stepik.org/users/1381287/certificates

certificates = get_certificates(USER)
print(f"Certificates: {len(certificates)}")

for cert in certificates:
    course_title = cert["course_title"]

    file_name = sanitize_filename(course_title) + ".pdf"
    file_name = DIR_CERTS / file_name
    if file_name.exists():
        continue

    print(
        f"Downloading certificate file for {course_title!r} course: {file_name.relative_to(DIR)}"
    )
    urlretrieve(cert["url"], file_name)
