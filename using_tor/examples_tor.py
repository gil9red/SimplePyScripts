# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
#
# __author__ = 'ipetrash'
#
#
# # # Released under CC0
# # import requesocks
# #
# # # Initialize a new wrapped requests object
# # session = requesocks.session()
# #
# # # Use Tor for both HTTP and HTTPS
# # session.proxies = {'http': 'socks5://localhost:9050', 'https': 'socks5://localhost:9050'}
# #
# # # fetch a page that shows your IP address
# # response = session.get('http://httpbin.org/ip')
# # print(response.text)
#
#
# # from urllib.request import build_opener
# # import socks
# # from sockshandler import SocksiPyHandler
# #
# # # All requests made by the opener will pass through the SOCKS proxy
# # opener = build_opener(SocksiPyHandler(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050))
# # print(opener.open('http://httpbin.org/ip'))
#
#
#
# # psw = '16:05834BCEDD478D1060F1D7E2CE98E9C13075E8D3061D702F63BCD674D1'
# #
# # from stem import Signal
# # from stem.control import Controller
# #
# #
# # # signal TOR for a new connection
# # def renew_connection():
# #     with Controller.from_port(port=9151) as controller:
# #         controller.authenticate(password=psw)
# #         controller.signal(Signal.NEWNYM)
# #
# #
# # renew_connection()
#
#
# # import socks
# # import socket
# import requests
# #
# # socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "localhost", 9050)
# # socket.socket = socks.socksocket
#
# from SocksiPy import socks
# # import socks
# s = socks.socksocket()
# s.setproxy(socks.PROXY_TYPE_SOCKS5,"localhost", 9050)
# # s.connect(('icanhazip.com', 80))
# s.connect(("www.sourceforge.net",80))
#
# r = requests.get('http://icanhazip.com')
# print(r.text)  # check ip
#
#
# # from stem.control import Controller
# #
# # with Controller.from_port(port = 9151) as controller:
# #   controller.authenticate()  # provide the password here if you set one
# #
# #   bytes_read = controller.get_info("traffic/read")
# #   bytes_written = controller.get_info("traffic/written")
# #
# #   print("My Tor relay has read %s bytes and written %s." % (bytes_read, bytes_written))
# #
# #
# # # opener = build_opener()
# # # print(opener.open('http://ifconfig.me/ip'))
# #
# #
# # import requests
# # print(requests.get('http://httpbin.org/ip').text)
# #
# # # import grab
# # #
# # # g = grab.Grab()
# # # g.go('http://httpbin.org/ip')
# # # print(g.response.body)
# # #


import sys

from PySide.QtGui import *
from PySide.QtCore import *
from PySide.QtWebKit import *
from PySide.QtNetwork import *


app = QApplication(sys.argv)

# Нужно запустить tor (например, Tor Browser) и указать порт
proxy = QNetworkProxy()
proxy.setType(QNetworkProxy.Socks5Proxy)
proxy.setHostName("localhost")
proxy.setPort(9050)
QNetworkProxy.setApplicationProxy(proxy)

view = QWebView()
# view.page().networkAccessManager().setProxy(proxy)
view.show()

# view.load('http://httpbin.org/ip')
view.load("https://2ip.ru/")
# view.load('http://myip.ru/')

sys.exit(app.exec_())
