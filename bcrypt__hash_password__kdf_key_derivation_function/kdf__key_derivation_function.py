#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/pyca/bcrypt
# SOURCE: https://en.wikipedia.org/wiki/Key_derivation_function


# pip install bcrypt
import bcrypt

# If "AttributeError: module 'bcrypt._bcrypt' has no attribute 'ffi'":
# pip uninstall py-bcrypt
# pip uninstall bcrypt
# pip install bcrypt


key = bcrypt.kdf(
    password=b"password",
    salt=b"salt",
    desired_key_bytes=32,
    rounds=100,
)
print(key)
# b'W\x1cq\xbd\xf25W\xf9\xe7\x99\x0fH\xfb\x1a-:n\xbd\x03\xd0\x1a>\x12\xa7\xf7\x0b\x85\x03\xc9\xf9\xbe8'
