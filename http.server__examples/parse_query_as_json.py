#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs


class BaseServer(BaseHTTPRequestHandler):
    def _set_headers(self) -> None:
        self.send_response(200)
        self.send_header("Content-type", "text/json; charset=utf-8")
        self.end_headers()

    def do_GET(self) -> None:
        self._set_headers()

        paths = urlparse(self.path)
        query = parse_qs(paths.query)
        for k, v in query.items():
            if len(v) == 1:
                query[k] = v[0]

        self.wfile.write(
            json.dumps(query, ensure_ascii=False, indent=4).encode("utf-8")
        )


def run(server_class=HTTPServer, handler_class=BaseServer, port=8080) -> None:
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
                urlopen(
                    "http://127.0.0.1:8080/?value=ipconfig&page=1&search=IPv4&a=1&b=1&a=2"
                )
                .read()
                .decode("utf-8")
            )
        ),
    ).start()
    # {
    #     "value": "ipconfig",
    #     "page": "1",
    #     "search": "IPv4",
    #     "a": [
    #         "1",
    #         "2"
    #     ],
    #     "b": "1"
    # }

    run()
