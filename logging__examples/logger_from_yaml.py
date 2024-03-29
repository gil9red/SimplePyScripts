#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging.config
from logging import getLogger
from pathlib import Path
from typing import Any

# pip install PyYAML
import yaml


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

log = getLogger("main")
log.debug("DEBUG")
log.info("INFO")

print()

log = getLogger("main2")
log.debug("DEBUG")
log.info("INFO")
