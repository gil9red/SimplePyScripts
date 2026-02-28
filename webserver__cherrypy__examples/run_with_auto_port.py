#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
from threading import Thread

import cherrypy


class RootServer:
    host = None
    port = None
    url = None

    def __init__(self) -> None:
        cherrypy.engine.subscribe("start", self.on_start)

    @cherrypy.expose
    def index(self) -> str:
        return f"{self.host}:{self.port} / {self.url}"

    def on_start(self) -> None:
        def _wait_server_running() -> None:
            # Wait running
            while not cherrypy.server.running:
                time.sleep(0.1)

            self.host, self.port = cherrypy.server.bound_addr
            self.url = cherrypy.server.description

            print(f"{self.host}:{self.port} / {self.url}")

        thread = Thread(target=_wait_server_running)
        thread.start()


if __name__ == "__main__":
    # Set random free port
    cherrypy.config.update({"server.socket_port": 0})

    cherrypy.quickstart(RootServer())
