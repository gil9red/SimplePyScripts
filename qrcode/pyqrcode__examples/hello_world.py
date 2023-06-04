#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://pythonhosted.org/PyQRCode/


# pip install pyqrcode
# pip install pypng
import pyqrcode


qr_code = pyqrcode.create("http://uca.edu")
qr_code.png("img.png")

qr_code = pyqrcode.create("Hello World!")
qr_code.png("img_hello.png")

qr_code.png("img_hello__scale=6.png", scale=6)
