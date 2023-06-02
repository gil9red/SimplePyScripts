#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os.path

import requests

import ca_certificate
from config import CA_CERT_FILE_PATH


if not os.path.exists(CA_CERT_FILE_PATH):
    ca_certificate.main()


DEBUG_LOG = False


proxies = {
    "http": "localhost:33333",
    "https": "localhost:33333",
}

# NOTE: When error "ssl.SSLError: [X509: KEY_VALUES_MISMATCH] key values mismatch (_ssl.c:3845)"
#       try remove all files from "C:\Users\<user>\.proxy\certificates"
for url in ["http://httpbin.org/headers", "https://httpbin.org/headers"]:
    print(url)

    # NOTE: The "verify" parameter is needed for HTTPS interception
    #       You can specify "verify=False", but there will be warnings
    rs = requests.get(url, proxies=proxies, verify=CA_CERT_FILE_PATH)

    DEBUG_LOG and print(rs)
    DEBUG_LOG and print(rs.url)
    DEBUG_LOG and print(rs.headers)
    DEBUG_LOG and print(rs.content)

    for header, value in rs.json()["headers"].items():
        if header.lower().startswith("x-my"):
            print(f"{header}: {value!r}")

    print()

"""
http://httpbin.org/headers
X-My-Client-Ip: '127.0.0.1'
X-My-Proxy: 'hell yeah!'

https://httpbin.org/headers
X-My-Client-Ip: '127.0.0.1'
X-My-Proxy: 'hell yeah!'
"""
