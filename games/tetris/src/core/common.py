#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
import sys

from .config import DEBUG


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/0360c558f85c0fe5e7320d88f90c0a4e23a7e342/seconds_to_str.py
def seconds_to_str(seconds: int | float) -> str:
    hh, mm = divmod(seconds, 3600)
    mm, ss = divmod(mm, 60)
    return "%02d:%02d:%02d" % (hh, mm, ss)


default_handler = logging.StreamHandler(stream=sys.stdout)
default_handler.setFormatter(
    logging.Formatter(
        "[%(asctime)s] %(filename)s:%(lineno)d %(levelname)-8s %(message)s"
    )
)

logger = logging.getLogger("tetris")
logger.setLevel(logging.DEBUG if DEBUG else logging.WARNING)
logger.addHandler(default_handler)
