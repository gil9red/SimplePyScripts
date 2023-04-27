#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/pyca/cryptography


# pip install cryptography
from cryptography.fernet import Fernet

# Put this somewhere safe!
key = Fernet.generate_key()

message = b"A really secret message. Not for prying eyes."

f = Fernet(key)
token = f.encrypt(message)
print(token)

de_message = f.decrypt(token)
print(de_message)  # b'A really secret message. Not for prying eyes.'
assert message == de_message
