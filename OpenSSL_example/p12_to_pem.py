#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from OpenSSL import crypto

p12_file_name = ''
p12_password = ''

# May require "" for empty password depending on version
p12 = crypto.load_pkcs12(open(p12_file_name, 'rb').read(), p12_password)

# PEM formatted private key
print(crypto.dump_privatekey(crypto.FILETYPE_PEM, p12.get_privatekey()))

# PEM formatted certificate
print(crypto.dump_certificate(crypto.FILETYPE_PEM, p12.get_certificate()))
