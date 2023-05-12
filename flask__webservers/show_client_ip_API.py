#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
import xml.etree.ElementTree as ET

from flask import Flask, request, Response


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    return request.remote_addr


@app.route("/json")
def get_json():
    return {
        "ip": request.remote_addr,
    }


@app.route("/xml")
def get_xml():
    root = ET.Element("ip")
    root.text = request.remote_addr
    xml_bytes = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    return Response(xml_bytes, mimetype="text/xml")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
