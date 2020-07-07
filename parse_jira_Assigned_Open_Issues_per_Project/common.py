#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import Dict

# For import ascii_table__simple_pretty__ljust.py
import sys

sys.path.append('..')
from ascii_table__simple_pretty__ljust import print_pretty_table


def print_table(assigned_open_issues_per_project: Dict[str, int]):
    data = [("PROJECT", 'Issues')] + list(assigned_open_issues_per_project.items())
    print_pretty_table(data)
    # PROJECT | Issues
    # --------+-------
    # xxx     | 1
    # yyy     | 2
    # zzz     | 3
