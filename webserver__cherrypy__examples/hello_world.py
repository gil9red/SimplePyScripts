#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install cherrypy
# https://github.com/cherrypy/cherrypy

import cherrypy


class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return "Hello World!"


if __name__ == '__main__':
    cherrypy.quickstart(HelloWorld())
