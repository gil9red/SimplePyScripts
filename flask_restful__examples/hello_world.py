#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://flask-restful.readthedocs.io/en/latest/quickstart.html#a-minimal-api


from flask import Flask

# pip install flask_restful
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class Echo(Resource):
    def get(self, text: str):
        return {'echo': text}


api.add_resource(HelloWorld, '/')
api.add_resource(Echo, '/echo/<string:text>')


if __name__ == '__main__':
    app.run(debug=True)
