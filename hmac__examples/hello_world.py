#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://docs.python.org/3.7/library/hmac.html


import hashlib
import hmac


key = b"<SECRET_KEY>"
msg = "Hello World!".encode("utf-8")

digest = hmac.new(key, msg, digestmod=hashlib.sha256).hexdigest()
text = "Now: " + digest
print(text)
# Now: 9a9e1262844d237c5fa17b839867ec3d49006a3639e4bd402008726474b12a76
