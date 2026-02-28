#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# pip install cherrypy
# https://github.com/cherrypy/cherrypy
import cherrypy


class HelloWorld:
    """Sample request handler class."""

    # Expose the index method through the web. CherryPy will never
    # publish methods that don't have the exposed attribute set to True.
    @cherrypy.expose
    def index(self) -> str:
        # CherryPy will call this method for the root URI ("/") and send
        # its return value to the client. Because this is tutorial
        # lesson number 01, we'll just send something really simple.
        # How about...
        return "Hello world!"


if __name__ == "__main__":
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().

    # Set port
    cherrypy.config.update({"server.socket_port": 9090})

    # Autoreload off
    cherrypy.config.update({"engine.autoreload.on": False})

    cherrypy.quickstart(HelloWorld())
