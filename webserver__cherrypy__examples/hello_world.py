#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# SOURCE: https://github.com/cherrypy/cherrypy/blob/master/cherrypy/tutorial/tut01_helloworld.py


# pip install cherrypy
# https://github.com/cherrypy/cherrypy
import cherrypy


class HelloWorld:
    """Sample request handler class."""

    # Expose the index method through the web. CherryPy will never
    # publish methods that don't have the exposed attribute set to True.
    @cherrypy.expose
    def index(self):
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

    # # Public IP
    # cherrypy.config.update({'server.socket_host': '0.0.0.0'})

    cherrypy.quickstart(HelloWorld())
