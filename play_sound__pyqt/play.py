#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
import sys

from main import play


if __name__ == "__main__":
    if len(sys.argv) > 1:
        play(sys.argv[1])
    else:
        file_name = os.path.basename(sys.argv[0])
        print(f"usage: {file_name} [-h] audio_file_name")
