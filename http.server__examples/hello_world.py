#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from http.server import BaseHTTPRequestHandler, HTTPServer


class HttpProcessor(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        self.send_response(200)
        self.send_header("content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(bytes("Hello!", "utf-8"))

    def do_POST(self) -> None:
        length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(length).decode("utf-8")
        print("post_data:", post_data)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes("Ok!", "utf-8"))


if __name__ == "__main__":
    server = HTTPServer(("localhost", 80), HttpProcessor)
    server.serve_forever()
