#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
import sys

from .config import DEBUG


default_handler = logging.StreamHandler(stream=sys.stdout)
default_handler.setFormatter(
    logging.Formatter(
        "[%(asctime)s] %(filename)s:%(lineno)d %(levelname)-8s %(message)s"
    )
)

logger = logging.getLogger("tetris")
logger.setLevel(logging.DEBUG if DEBUG else logging.WARNING)
logger.addHandler(default_handler)
