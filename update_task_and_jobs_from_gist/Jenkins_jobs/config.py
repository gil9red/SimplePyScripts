#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
from pathlib import Path


DIR = Path(__file__).resolve().parent


def get_from_environ_or_file(name: str, default: str = None) -> str:
    try:
        return (
            os.environ.get(name)
            or (DIR / f"{name}.txt").read_text("utf-8")
        ).strip()

    except Exception as e:
        if default:
            return default

        raise e


GIST_URL = get_from_environ_or_file("GIST_URL")

JENKINS_URL = get_from_environ_or_file("JENKINS_URL", default="http://127.0.0.1:8080/")

TOKEN = get_from_environ_or_file("TOKEN")
LOGIN, PASSWORD = TOKEN.split("=")  # NOTE: PASSWORD: password or token api
