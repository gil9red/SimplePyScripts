#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from typing import Any


# SOURCE: https://github.com/encode/uvicorn/blob/d79f285184404694c77f7ca649858e7488270cf7/uvicorn/config.py#L66
#         Added fmt="[%(asctime)s] "
LOGGING_CONFIG: dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "[%(asctime)s] %(levelprefix)s %(message)s",
            "use_colors": None,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": '[%(asctime)s] %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',  # noqa: E501
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "uvicorn": {"handlers": ["default"], "level": "INFO", "propagate": False},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
    },
}


if __name__ == "__main__":
    import yaml
    yaml.dump(
        LOGGING_CONFIG,
        open("logging_config.yml", mode="w", encoding="utf-8"),
        sort_keys=False,
    )
