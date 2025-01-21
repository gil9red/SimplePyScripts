#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/nneonneo/universal-doom/blob/main/DOOM1.WAD


from pathlib import Path
from urllib.request import urlretrieve


url = "https://github.com/nneonneo/universal-doom/raw/refs/heads/main/DOOM1.WAD"
path = Path(__file__).parent.resolve() / Path(url).name
print(f"Download to {path}")

urlretrieve(url, path)
