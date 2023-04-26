#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import socket
from config import *


# URL_NG_SERVER = 'http://10.7.8.31:12000'
HOST = URL_NG_SERVER.replace("https://", "").replace("http://", "")

# HOST = 10.7.8.31, PORT = 12000
HOST, PORT = HOST.split(":")
PORT = int(PORT)


post_data = """
<?xml version="1.0"?>
<REQUEST OBJECT_CLASS="TAbonentObject" ACTION="GET_CHANGES" VERSION="0" TYPE_VERSION="I" PACK="ZLIB"
INT_SOFT_ID="{INT_SOFT_ID}"
POINT_CODE="{POINT_CODE}"
SignOut="No"
ExpectSigned="No"
/>
""".format(
    INT_SOFT_ID=INT_SOFT_ID, POINT_CODE=POINT_CODE
)


http_request = (
    "POST / HTTP/1.1\r\n",
    "Host: {host}:{port}\r\n",
    "Accept-Encoding: gzip, deflate\r\n",
    "User-Agent: {user_agent}\r\n",
    "Connection: close\r\n",
    "Accept: */*\r\n",
    "Content-Length: {content_length}\r\n",
    "\r\n",
    "{body}",
)
http_request = "".join(http_request)
http_request = http_request.format(
    host=HOST,
    port=PORT,
    user_agent="iHuman",
    content_length=len(post_data),
    body=post_data,
)

print(repr(http_request))


sock = socket.socket()
sock.connect((HOST, PORT))
sock.send(http_request.encode())

print("Socket name: {}".format(sock.getsockname()))
print("\nResponse:")

while True:
    data = sock.recv(1024)
    if not data:
        break

    print(len(data), data)
