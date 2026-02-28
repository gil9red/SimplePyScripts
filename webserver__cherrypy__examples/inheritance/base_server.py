#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
from typing import Any

# pip install cherrypy
# https://github.com/cherrypy/cherrypy
import cherrypy


class BaseServer:
    expose = cherrypy.expose
    json_in = cherrypy.tools.json_in()
    json_out = cherrypy.tools.json_out()

    def __init__(self) -> None:
        # Set a custom response for errors.
        self._cp_config = {"error_page.default": self.all_exception_handler}
        # # OR:
        # Root._cp_config = {'error_page.default': Root.all_exception_handler}

        self.name = "BaseServer"

    @cherrypy.expose
    def get_name(self) -> str:
        return self.name

    @cherrypy.expose
    def execute(self) -> Any:
        return "Not implement"

    @cherrypy.expose
    def execute_func(self) -> str:
        return self._execute_func()

    def _execute_func(self) -> str:
        return "Not implement"

    # Expose the index method through the web. CherryPy will never
    # publish methods that don't have the exposed attribute set to True.
    @cherrypy.expose
    def index(self) -> str:
        return f"""
            This is: <b>{self.name}</b><br>
            <a href="/error">Get error</a><br>
            <a href="/execute">Execute</a><br>
            <a href="/execute_func">Execute func</a><br>
            <a href="/get_name">Get name</a>
        """

    @cherrypy.expose
    def error(self) -> str:
        _ = 1 / 0

        return "Bad!"

    def all_exception_handler(self, status, message, traceback, version) -> str:
        response = cherrypy.response
        response.headers["Content-Type"] = "application/json"

        return json.dumps(
            {
                "about": "Catch error!",
                "status": status,
                "message": message,
                "text": traceback.strip().split("\n")[-1],
                "traceback": traceback,
                "server_name": self.name,
            }
        )

    def run(self, port=9090) -> None:
        # Set port
        cherrypy.config.update({"server.socket_port": port})

        # Autoreload off
        cherrypy.config.update({"engine.autoreload.on": False})

        cherrypy.quickstart(self)


if __name__ == "__main__":
    server = BaseServer()
    server.run(port=9090)
