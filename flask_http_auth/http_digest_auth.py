#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json

from pathlib import Path

# pip install flask
from flask import Flask

# pip install Flask-HTTPAuth
from flask_httpauth import HTTPDigestAuth


DIR = Path(__file__).resolve().parent
PATH_USERS = DIR / "users.json"

users = json.loads(PATH_USERS.read_text("utf-8"))


app = Flask(__name__)
app.config["SECRET_KEY"] = "<SECRET_KEY_HERE>"

auth = HTTPDigestAuth()


@auth.get_password
def get_password(username: str) -> str | None:
    return users.get(username)


@app.route("/")
@auth.login_required
def index():
    return f"Hello, {auth.username()}!"


if __name__ == "__main__":
    app.run()
