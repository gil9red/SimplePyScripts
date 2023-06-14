#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path
from common import get_chart


PATH = Path(__file__).resolve().absolute()
FILE_NAME = Path(f"{PATH}.png")


qc = get_chart()
qc.to_file(FILE_NAME)
