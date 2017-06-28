#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import uuid

# make a UUID based on the host ID and current time
print(uuid.uuid1())  # UUID('a8098c1a-f86e-11da-bd1a-00112444be1e')

# make a UUID using an MD5 hash of a namespace UUID and a name
print(uuid.uuid3(uuid.NAMESPACE_DNS, 'python.org'))  # UUID('6fa459ea-ee8a-3ca4-894e-db77e160355e')

# make a random UUID
print(uuid.uuid4())  # UUID('16fd2706-8baf-433b-82eb-8c7fada847da')

# make a UUID using a SHA-1 hash of a namespace UUID and a name
print(uuid.uuid5(uuid.NAMESPACE_DNS, 'python.org'))  # UUID('886313e1-3b8a-5372-9b90-0c9aee199e5d')

print()
print('From UUID / GUID')
# make a UUID from a string of hex digits (braces and hyphens ignored)
x = uuid.UUID('{00010203-0405-0607-0809-0a0b0c0d0e0f}')

# convert a UUID to a string of hex digits in standard form
print(str(x))  # '00010203-0405-0607-0809-0a0b0c0d0e0f'

# get the raw 16 bytes of the UUID
print(x.bytes)  # '\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'

# make a UUID from a 16-byte string
print(uuid.UUID(bytes=x.bytes))  # UUID('00010203-0405-0607-0809-0a0b0c0d0e0f')
