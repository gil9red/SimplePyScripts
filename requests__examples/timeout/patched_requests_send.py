#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests

TIMEOUT: float = 60


if not hasattr(requests.Session.send, "_is_patched"):
    original_requests_send = requests.Session.send

    def patched_requests_send(self, request, **kwargs):
        if kwargs.get("timeout") is None:
            kwargs["timeout"] = TIMEOUT
        return original_requests_send(self, request, **kwargs)

    patched_requests_send._is_patched = True
    requests.Session.send = patched_requests_send


session = requests.session()

rs = session.get("https://httpbin.org/delay/1")
print(rs)

rs = session.get("https://httpbin.org/delay/2")
print(rs)

rs = session.get("https://httpbin.org/delay/3")
print(rs)
