#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging

from config import DEBUG


logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.WARNING,
    format="[%(asctime)s] %(filename)s:%(lineno)d %(levelname)-8s %(message)s",
)
logger = logging.getLogger(__file__)
