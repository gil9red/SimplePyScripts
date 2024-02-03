#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests


HTTP_TIMEOUT = 60


# SOURCE: https://stackoverflow.com/a/47384155/5909792
class TimeoutRequestsSession(requests.Session):
    def request(self, *args, **kwargs):
        kwargs.setdefault('timeout', HTTP_TIMEOUT)
        return super().request(*args, **kwargs)


session = TimeoutRequestsSession()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"
