#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json

# pip install cherrypy
# https://github.com/cherrypy/cherrypy
import cherrypy


class Root:
    def __init__(self) -> None:
        # Set a custom response for errors.
        self._cp_config = {"error_page.default": Root.all_exception_handler}
        # # OR:
        # Root._cp_config = {'error_page.default': Root.all_exception_handler}

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
        _ = 1 / 0

        return "Bad!"

    @staticmethod
    def all_exception_handler(status, message, traceback, version):
        response = cherrypy.response
        response.headers["Content-Type"] = "application/json"

        return json.dumps(
            {
                "about": "Catch error!",
                "status": status,
                "message": message,
                "text": traceback.strip().split("\n")[-1],
                "traceback": traceback,
                "version": version,
            }
        )


if __name__ == "__main__":
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().

    # Set port
    cherrypy.config.update({"server.socket_port": 9090})

    # Autoreload off
    cherrypy.config.update({"engine.autoreload.on": False})

    cherrypy.quickstart(Root())
