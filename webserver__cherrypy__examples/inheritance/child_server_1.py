#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from base_server import BaseServer


class ChildServer(BaseServer):
    def __init__(self):
        super().__init__()

        self.name = "ChildServer_1"

    @BaseServer.expose
    def execute(self):
        return "ChildServer_1.execute!"

    def _execute_func(self):
        return "ChildServer_1 _execute_func"

    @BaseServer.expose
    def error(self):
        raise Exception("ChildServer_1 EXCEPTION!")


if __name__ == "__main__":
    server = ChildServer()
    server.run(port=9091)
