#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/pyca/bcrypt


# pip install bcrypt
import bcrypt

# If "AttributeError: module 'bcrypt._bcrypt' has no attribute 'ffi'":
# pip uninstall py-bcrypt
# pip uninstall bcrypt
# pip install bcrypt


password = b"super secret password"

# Hash a password for the first time, with a randomly-generated salt
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
print(hashed)

# Check that an unhashed password matches one that has previously been hashed
if bcrypt.checkpw(password, hashed):
    print("It Matches!")
else:
    print("It Does not Match :(")
