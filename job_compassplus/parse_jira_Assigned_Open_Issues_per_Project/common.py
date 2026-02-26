#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
import sys

from logging.handlers import RotatingFileHandler
from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

# pip install tabulate
from tabulate import tabulate


def get_table(assigned_open_issues_per_project: dict[str, int]) -> str:
    return tabulate(
        list(assigned_open_issues_per_project.items()),
        headers=("PROJECT", "Issues"),
        tablefmt="grid",
    )


def print_table(assigned_open_issues_per_project: dict[str, int]) -> None:
    print(get_table(assigned_open_issues_per_project))
    # PROJECT | Issues
    # --------+-------
    # xxx     | 1
    # yyy     | 2
    # zzz     | 3


def get_logger(
    name, file="log.txt", encoding="utf-8", log_stdout=True, log_file=True
) -> logging.Logger:
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "[%(asctime)s] %(filename)s:%(lineno)d %(levelname)-8s %(message)s"
    )

    if log_file:
        fh = RotatingFileHandler(
            file, maxBytes=10_000_000, backupCount=5, encoding=encoding
        )
        fh.setFormatter(formatter)
        log.addHandler(fh)

    if log_stdout:
        sh = logging.StreamHandler(stream=sys.stdout)
        sh.setFormatter(formatter)
        log.addHandler(sh)

    return log


logger = get_logger("parse_jira_Assigned_Open_Issues_per_Project")
