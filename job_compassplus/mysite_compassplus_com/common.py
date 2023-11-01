#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
from pathlib import Path

# pip install requests_ntlm2
from requests_ntlm2 import HttpNtlmAuth

from requests import Response

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(ROOT_DIR))
from root_common import session

from config import USERNAME, PASSWORD


URL = "https://mysite.compassplus.com/Person.aspx?accountname={}"


def do_get(url: str, *args, **kwargs) -> Response:
    rs = session.get(
        url,
        auth=HttpNtlmAuth(USERNAME, PASSWORD),
        *args,
        **kwargs
    )
    rs.raise_for_status()
    return rs
