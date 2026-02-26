#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from http.server import BaseHTTPRequestHandler, HTTPServer


class HttpProcessor(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        user_agent = self.headers["User-Agent"]
        print(user_agent)

        self.send_response(200)
        self.send_header("content-type", "text/html; charset=utf-8")
        self.end_headers()

        html = user_agent

        self.wfile.write(bytes(html, "utf-8"))


if __name__ == "__main__":
    host, port = "localhost", 80
    print(f"Running on http://{host}:{port}/")

    server = HTTPServer((host, port), HttpProcessor)
    server.serve_forever()
