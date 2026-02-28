#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import cherrypy


class RootServer:
    def __init__(self) -> None:
        self.running = False

        cherrypy.engine.subscribe("start", self.on_start)
        cherrypy.engine.subscribe("stop", self.on_stop)
        cherrypy.engine.subscribe("exit", self.on_exit)

    def on_start(self) -> None:
        print("start")
        self.running = True

        # Exit!
        cherrypy.engine.exit()

    def on_stop(self) -> None:
        print("stop")
        self.running = False

    def on_exit(self) -> None:
        print("exit")


if __name__ == "__main__":
    # Set port
    cherrypy.config.update({"server.socket_port": 9090})

    cherrypy.quickstart(RootServer())
