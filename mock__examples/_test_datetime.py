#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from datetime import datetime


def get() -> tuple[datetime, datetime]:
    return datetime.now(), datetime.utcnow()
