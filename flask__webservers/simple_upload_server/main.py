#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from flask import Flask, request


app = Flask(__name__)


@app.route("/", methods=["POST"])
def index() -> str:
    file = request.files["file"]
    # file.save(file.filename)
    # OR:
    file.save("upload_file.txt")

    return "ok"


if __name__ == "__main__":
    app.run(
        port=6000,
    )
