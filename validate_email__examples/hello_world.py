#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install validate_email
# pip install pyDNS
from validate_email import validate_email

# NOTE: Fix for "No working name servers discovered"
import DNS


DNS.defaults["server"] = ["8.8.8.8", "8.8.4.4"]

# TODO: pip install pyDNS:
#           ImportError: No module named 'Type'
#
#       Use: pip install py3dns


email = "example@inbox.ru"

# Basic usage:
is_valid = validate_email(email)
print(is_valid)

# Check if the host has SMTP Server:
is_valid = validate_email(email, check_mx=True)
print(is_valid)

# Check if the host has SMTP Server and the email really exists:
is_valid = validate_email(email, verify=True)
print(is_valid)
