#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# pip install cherrypy
# https://github.com/cherrypy/cherrypy

import cherrypy


class RootServer:
    @cherrypy.expose
    def index(self) -> str:
        return """
<html>
    <head>
        <script type="text/javascript" src="jquery 1.4.2.min.js"></script>
    </head>

    <body>
        <a href="jquery 1.4.2.min.js">Open jquery 1.4.2.min.js</a>     
    </body>
</html>
"""


if __name__ == "__main__":
    import pathlib

    # Autoreload off
    cherrypy.config.update({"engine.autoreload.on": False})

    # Set port
    cherrypy.config.update({"server.socket_port": 9090})

    # # Public IP
    # cherrypy.config.update({'server.socket_host': '0.0.0.0'})

    static_dir = str((pathlib.Path(__file__).parent / "static").resolve())

    # For include css, js in html
    cherrypy.config.update(
        {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": static_dir,
        }
    )

    cherrypy.quickstart(RootServer())
