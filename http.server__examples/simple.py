#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from http.server import BaseHTTPRequestHandler, HTTPServer


class BaseServer(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write(
            "<html><body><p>hello, world!</p></body></html>".encode("utf-8")
        )

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        self._set_headers()
        self.wfile.write(
            "<html><body><p>POST!</p><p>%s</p></body></html>".encode("utf-8")
            % post_data
        )


def run(server_class=HTTPServer, handler_class=BaseServer, port=8080):
    print(f"HTTP server running on http://127.0.0.1:{port}")

    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    run()
