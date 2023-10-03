#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
from pathlib import Path

# pip install requests_ntlm2
from requests_ntlm2 import HttpNtlmAuth

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(ROOT_DIR))
from root_common import session

from config import USERNAME, PASSWORD


URL = "https://mysite.compassplus.com/Person.aspx?accountname={}"


session.auth = HttpNtlmAuth(USERNAME, PASSWORD)
