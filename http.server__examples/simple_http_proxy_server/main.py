#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from http.server import HTTPServer, SimpleHTTPRequestHandler
import requests


class ProxyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/'):
            super().do_GET()
            return

        # NOTE: Add custom header
        self.headers.add_header('x-my-proxy', 'hell yeah!')
        self.headers.add_header('x-my-client-ip', self.client_address[0])

        rs = requests.get(self.path, headers=self.headers)

        # We remove this header, since already decoded data in rs.content
        rs.headers['Content-Encoding'] = ''

        self.send_response(rs.status_code)

        for header, value in rs.headers.items():
            self.send_header(header, value)
        self.end_headers()

        self.wfile.write(rs.content)


def http_proxy(host: str, port: int):
    print(f'Server listening at http://{host}:{port}')

    server_http = HTTPServer((host, port), ProxyHandler)
    server_http.serve_forever()


if __name__ == '__main__':
    host = "localhost"
    port = 33333

    http_proxy(host, port)
