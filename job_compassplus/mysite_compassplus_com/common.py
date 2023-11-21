#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import time

from pathlib import Path

# pip install requests_ntlm2
from requests_ntlm2 import HttpNtlmAuth

from requests import Response
from requests.exceptions import RequestException

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(ROOT_DIR))
from root_common import session

from config import USERNAME, PASSWORD


URL = "https://mysite.compassplus.com/Person.aspx?accountname={}"


def do_get(url: str, *args, **kwargs) -> Response:
    attempts = 0
    max_attempts = 5

    while True:
        attempts += 1
        try:
            rs = session.get(
                url,
                auth=HttpNtlmAuth(USERNAME, PASSWORD),
                *args,
                **kwargs
            )

            # Через какое-то отваливается доступ, скорее всего, нужно куки чистить
            if rs.status_code == 401:
                session.cookies.clear()

            rs.raise_for_status()

            return rs

        except RequestException as e:
            if attempts >= max_attempts:
                raise e

        time.sleep(5)  # 5 seconds
