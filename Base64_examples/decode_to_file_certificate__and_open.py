#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os

from decode_to_file import decode_base64_to_file


FILE_NAME = "cert.cer"
TEXT = """
MIIBeTCCASigAwIBAgIEBoLBizAIBgYqhQMCAgMwMTELMAkGA1UEBhMCUlUxEjAQBgNVBAoMCUNy
eXB0b1BybzEOMAwGA1UEAwwFQWxpYXMwHhcNMTcwNjA3MDk1MzM5WhcNMTgwNjA3MDk1MzM5WjAx
MQswCQYDVQQGEwJSVTESMBAGA1UECgwJQ3J5cHRvUHJvMQ4wDAYDVQQDDAVBbGlhczBjMBwGBiqF
AwICEzASBgcqhQMCAiMBBgcqhQMCAh4BA0MABEC3lLP1IrUG4RgOXu3Vd2mwATIL7DdnIi6k6jce
cDZZrFy3mcRiMouQq3VNxoJmvRPMGEsraYnR439VxNpgyF2JoyYwJDAOBgNVHQ8BAf8EBAMCBsAw
EgYDVR0TAQH/BAgwBgEB/wIBBTAIBgYqhQMCAgMDQQAfz80NqU78fkj7/WBnA19YI4QYkDPX0l77
l1hnV3Acv5f+WLhiKblVW1gZnNjhmnacgFQo5xb3UimMqgroonZz
"""

decode_base64_to_file(FILE_NAME, TEXT)

# Open file
os.startfile(FILE_NAME)
