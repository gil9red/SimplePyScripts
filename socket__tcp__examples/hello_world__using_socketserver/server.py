#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://docs.python.org/3.6/library/socketserver.html#socketserver-tcpserver-example


import socketserver

import sys
sys.path.append("..")
from common import send_msg, recv_msg


HOST, PORT = "localhost", 9090


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self) -> None:
        print("Connected:", self.client_address)

        data = recv_msg(self.request)
        print(f"Receiving ({len(data)}): {data}")

        print("Sending")
        send_msg(self.request, data.upper())

        print("Close\n")


if __name__ == "__main__":
    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        print(f"Server: {server.server_address}")

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
