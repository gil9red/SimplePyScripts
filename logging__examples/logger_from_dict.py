#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging.config
from logging import getLogger
from pathlib import Path
from typing import Any


DIR_LOGS: Path = Path(__file__).resolve().parent / "logs"
DIR_LOGS.mkdir(parents=True, exist_ok=True)


LOGGING: dict[str, Any] = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(name)-10s %(filename)s[LINE:%(lineno)d] %(levelname)-8s %(message)s",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "default",
        },
        "main-file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "main.log",
            "maxBytes": 10_000_000,
            "backupCount": 5,
            "encoding": "utf-8",
            "formatter": "default",
        },
        "main2-file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "main2.log",
            "maxBytes": 10_000_000,
            "backupCount": 5,
            "encoding": "utf-8",
            "formatter": "default",
        },
    },
    "loggers": {
        "main": {
            "level": "DEBUG",
            "handlers": [
                "console",
                "main-file",
            ]
        },
        "main2": {
            "level": "INFO",
            "handlers": [
                "console",
                "main2-file",
            ]
        },
    },
}
for handler in LOGGING["handlers"].values():
    try:
        handler["filename"] = DIR_LOGS / handler["filename"]
    except KeyError:
        pass


logging.config.dictConfig(LOGGING)

log = getLogger("main")
log.debug("DEBUG")
log.info("INFO")

print()

log = getLogger("main2")
log.debug("DEBUG")
log.info("INFO")
