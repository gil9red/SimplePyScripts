#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import cherrypy


class RootServer:
    host = None
    port = None
    url = None

    def __init__(self):
        cherrypy.engine.subscribe('start', self.on_start)

    @cherrypy.expose
    def index(self):
        return f'{self.host}:{self.port} / {self.url}'

    def on_start(self):
        def _wait_server_running():
            import time

            # Wait running
            while not cherrypy.server.running:
                time.sleep(0.1)

            self.host, self.port = cherrypy.server.bound_addr
            self.url = cherrypy.server.description

            print(f'{self.host}:{self.port} / {self.url}')

        from threading import Thread
        thread = Thread(target=_wait_server_running)
        thread.start()


if __name__ == '__main__':
    # Set random free port
    cherrypy.config.update({'server.socket_port': 0})

    cherrypy.quickstart(RootServer())
