#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/cherrypy/cherrypy/blob/master/cherrypy/tutorial/tut02_expose_methods.py


import cherrypy


class HelloWorld:
    @cherrypy.expose
    def index(self) -> str:
        # Let's link to another method here.
        return 'We have an <a href="show_msg">important message</a> for you!'

    @cherrypy.expose
    def show_msg(self) -> str:
        # Here's the important message!
        return "Hello world!"


if __name__ == "__main__":
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().
    cherrypy.quickstart(HelloWorld())
