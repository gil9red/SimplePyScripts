#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = "ipetrash"


# pip install cherrypy
# https://github.com/cherrypy/cherrypy
import cherrypy


class HelloWorld:
    """Sample request handler class."""

    # NOTE: try http://127.0.0.1:9090/?a=1&b=2&c=123
    @cherrypy.expose
    def index(self, **kwargs):
        return f"Hello world!: {kwargs}"


if __name__ == "__main__":
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().

    # Set port
    cherrypy.config.update({"server.socket_port": 9090})

    # # Public IP
    # cherrypy.config.update({'server.socket_host': '0.0.0.0'})

    cherrypy.quickstart(HelloWorld())
