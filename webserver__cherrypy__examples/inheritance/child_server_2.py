#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from base_server import BaseServer


class ChildServer(BaseServer):
    def __init__(self):
        super().__init__()

        self.name = "ChildServer_2"

    @BaseServer.expose
    @BaseServer.json_out
    def execute(self):
        return {
            "text": "ChildServer_2.execute!",
        }

    @BaseServer.expose
    def error(self):
        _ = list()[0]


if __name__ == "__main__":
    server = ChildServer()
    server.run(port=9092)
