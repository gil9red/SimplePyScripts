#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
import sys

from logging.handlers import RotatingFileHandler
from pathlib import Path

from flask import Flask

from utils import FilterRemoveDateFromWerkzeugLogs


DIR_LOGS: Path = Path(__file__).resolve().parent / "logs"
DIR_LOGS.mkdir(parents=True, exist_ok=True)


app = Flask(__name__)

formatter = logging.Formatter(
    "[%(asctime)s] %(filename)s:%(lineno)d %(levelname)-8s %(message)s"
)

file_handler = RotatingFileHandler(
    DIR_LOGS / "main_old.log", maxBytes=10_000_000, backupCount=5, encoding="utf-8"
)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler(stream=sys.stdout)
stream_handler.setFormatter(formatter)

log: logging.Logger = app.logger
log.handlers.clear()
log.setLevel(logging.DEBUG)
log.addHandler(file_handler)
log.addHandler(stream_handler)

log_werkzeug = logging.getLogger("werkzeug")
log_werkzeug.setLevel(logging.DEBUG)
log_werkzeug.addHandler(file_handler)
log_werkzeug.addHandler(stream_handler)
log_werkzeug.addFilter(FilterRemoveDateFromWerkzeugLogs())


@app.route("/")
def index() -> str:
    log.debug("call index")
    return "Hello World!"


if __name__ == "__main__":
    app.debug = True

    app.run(host="0.0.0.0", port=5000)
