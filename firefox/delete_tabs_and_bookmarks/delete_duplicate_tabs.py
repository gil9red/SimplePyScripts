#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))

import api
from common import get_logger
from config import file_name_session


log = get_logger(__file__, DIR / "logs")


log.info("Start")
api.close_duplicate_tabs(file_name_session, log)
log.info("Finish")
