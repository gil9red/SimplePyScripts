#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import logging
import sys

from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Dict

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

# For import ascii_table__simple_pretty__ljust.py
sys.path.append(str(ROOT_DIR.parent))
from ascii_table__simple_pretty__ljust import pretty_table


def get_table(assigned_open_issues_per_project: Dict[str, int]) -> str:
    data = [("PROJECT", 'Issues')] + list(assigned_open_issues_per_project.items())
    return pretty_table(data)


def print_table(assigned_open_issues_per_project: Dict[str, int]):
    print(get_table(assigned_open_issues_per_project))
    # PROJECT | Issues
    # --------+-------
    # xxx     | 1
    # yyy     | 2
    # zzz     | 3


def get_logger(name, file='log.txt', encoding='utf-8', log_stdout=True, log_file=True) -> logging.Logger:
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] %(filename)s:%(lineno)d %(levelname)-8s %(message)s')

    if log_file:
        fh = RotatingFileHandler(file, maxBytes=10000000, backupCount=5, encoding=encoding)
        fh.setFormatter(formatter)
        log.addHandler(fh)

    if log_stdout:
        sh = logging.StreamHandler(stream=sys.stdout)
        sh.setFormatter(formatter)
        log.addHandler(sh)

    return log


logger = get_logger('parse_jira_Assigned_Open_Issues_per_Project')
