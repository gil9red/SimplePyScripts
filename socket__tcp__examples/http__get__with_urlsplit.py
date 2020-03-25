#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from urllib.parse import urlsplit
import socket
import re

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# url = input ("Enter a url: ")
url = 'http://google.ru/'
try:
    re.search("^http[s]?://.*?", url)
except:
    print("Error")

result = urlsplit(url)
print(result)

socket.connect((result.netloc, 80))

cmd = f'GET {result.path} HTTP/1.0\r\n\r\n'.encode()
print(cmd)
socket.send(cmd)

while True:
    data = socket.recv(512)
    if not len(data):
        break
    print(data, end='')

socket.close()
