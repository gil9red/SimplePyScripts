#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from ftplib import FTP


# Connect to host, default port
ftp = FTP("ftp.debian.org")
print(ftp.host)

# User anonymous, passwd anonymous
print(ftp.login())

# Change into "debian" directory
print(ftp.cwd("debian"))

# List directory contents
print(ftp.retrlines("LIST"))

# Show file content
print(ftp.retrbinary("RETR README", lambda data: print(repr(data))))

# Download file
print(ftp.retrbinary("RETR README", open("README", "wb").write))

# Send a QUIT command to the server and close the connection
print(ftp.quit())
