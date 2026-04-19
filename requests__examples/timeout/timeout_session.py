#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests

TIMEOUT: float = 60


class TimeoutRequestsSession(requests.Session):
    def request(self, *args, **kwargs):
        kwargs.setdefault("timeout", TIMEOUT)
        return super().request(*args, **kwargs)


session = TimeoutRequestsSession()

rs = session.get("https://httpbin.org/delay/1")
print(rs)

rs = session.get("https://httpbin.org/delay/2")
print(rs)

rs = session.get("https://httpbin.org/delay/3")
print(rs)
