#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging.config
from pathlib import Path
from typing import Any

# pip install PyYAML
import yaml

from flask import Flask


DIR: Path = Path(__file__).resolve().parent

DIR_LOGS: Path = DIR / "logs"
DIR_LOGS.mkdir(parents=True, exist_ok=True)

CONFIG_LOG_FILE_NAME: Path = DIR / "log-config.yaml"


LOGGING: dict[str, Any] = yaml.safe_load(
    CONFIG_LOG_FILE_NAME.read_text("utf-8")
)
for handler in LOGGING["handlers"].values():
    try:
        handler["filename"] = DIR_LOGS / handler["filename"]
    except KeyError:
        pass

logging.config.dictConfig(LOGGING)

log = logging.getLogger("werkzeug")


app = Flask(__name__)
app.logger = log


@app.route("/")
def index() -> str:
    log.debug("call index")
    return "Hello World!"


if __name__ == "__main__":
    app.debug = True

    app.run(host="0.0.0.0", port=5000)
