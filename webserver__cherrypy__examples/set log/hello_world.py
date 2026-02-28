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
    def index(self) -> str:
        # CherryPy will call this method for the root URI ("/") and send
        # its return value to the client. Because this is tutorial
        # lesson number 01, we'll just send something really simple.
        # How about...
        return 'Hello world!<br><a href="/error">Get error</a>'

    @cherrypy.expose
    def error(self) -> str:
        1 / 0

        return "Bad!"


if __name__ == "__main__":
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().

    # Set port
    cherrypy.config.update({"server.socket_port": 9090})

    # Set log file
    cherrypy.config.update(
        {
            "log.error_file": "web.log",
            "log.access_file": "access.log",
        }
    )

    cherrypy.quickstart(HelloWorld())
