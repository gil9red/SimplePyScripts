#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path

# pip install show-in-file-manager==1.1.6
from showinfm import show_in_file_manager


current_file: Path = Path(__file__).resolve()
# show_in_file_manager(current_file)  # NOTE: TypeError: 'WindowsPath' object is not iterable
show_in_file_manager(str(current_file))
