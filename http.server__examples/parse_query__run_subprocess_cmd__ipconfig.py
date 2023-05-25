#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import subprocess

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs


class BaseServer(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

    def do_GET(self):
        self._set_headers()

        paths = urlparse(self.path)
        query = parse_qs(paths.query)
        value = query["value"][0]

        result = subprocess.check_output(
            value, encoding="CP866", shell=True, universal_newlines=True
        )
        self.wfile.write(result.encode("utf-8"))


def run(server_class=HTTPServer, handler_class=BaseServer, port=8080):
    print(f"HTTP server running on http://127.0.0.1:{port}")

    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    from threading import Timer
    from urllib.request import urlopen

    # Start in 2 seconds
    Timer(
        2,
        lambda: (
            print(
                urlopen("http://127.0.0.1:8080/?value=ipconfig").read().decode("utf-8")
            )
        ),
    ).start()

    run()
