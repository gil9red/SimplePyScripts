#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/abhinavsingh/proxy.py#tls-interception

# NOTE: When error "ssl.SSLError: [X509: KEY_VALUES_MISMATCH] key values mismatch (_ssl.c:3845)"
#       try remove all files from "C:\Users\<user>\.proxy\certificates"


import os.path

import ca_certificate

from config import CA_KEY_FILE_PATH, CA_CERT_FILE_PATH, CA_SIGNING_KEY_FILE_PATH
from hello_world import main


if not os.path.exists(CA_CERT_FILE_PATH):
    ca_certificate.main()


if __name__ == '__main__':
    main(
        ca_key_file=CA_KEY_FILE_PATH,
        ca_cert_file=CA_CERT_FILE_PATH,
        ca_signing_key_file=CA_SIGNING_KEY_FILE_PATH,
    )
