#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlsplit

from get_info_html import get_info_html


class HttpProcessor(BaseHTTPRequestHandler):
    def do_GET(self):
        o = urlsplit(self.path)

        # Only index
        if o.path != "/":
            self.send_error(404)
            return

        text = get_info_html()

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Connection", "close")
        self.end_headers()

        self.wfile.write(text.encode("utf-8"))


def run(server_class=HTTPServer, handler_class=HttpProcessor, port=8080):
    print(f"HTTP server running on http://127.0.0.1:{port}")

    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    run(
        port=int(os.environ.get("PORT", 50012)),
    )
