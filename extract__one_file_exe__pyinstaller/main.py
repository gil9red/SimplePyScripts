#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
import shutil
import subprocess
import sys

from pathlib import Path
from urllib.request import urlretrieve


# SOURCE: https://github.com/extremecoders-re/pyinstxtractor
# SOURCE: https://github.com/rocky/python-uncompyle6


print("START: INSTALL SCRIPTS")
subprocess.call(["pip", "install", "uncompyle6"])
urlretrieve(
    "https://raw.githubusercontent.com/extremecoders-re/pyinstxtractor/master/pyinstxtractor.py",
    "pyinstxtractor.py",
)
print("FINISH: INSTALL SCRIPTS")

print("\n" + "-" * 100 + "\n")

print("START: BUILD EXE")
subprocess.call(["pyinstaller", "--clean", "--onefile", "_test_file.py"])

shutil.rmtree("build")
os.remove("_test_file.spec")
print("FINISH: BUILD EXE")

print("\n" + "-" * 100 + "\n")

print("START: UNPACK EXE")
subprocess.call([sys.executable, "pyinstxtractor.py", "dist/_test_file.exe"])
print("FINISH: UNPACK EXE")

print("\n" + "-" * 100 + "\n")

print("START: CONVERT PYC TO PY")
source_test_file = Path("_source_test_file.py")
subprocess.call([
    "uncompyle6",
    "-o",
    str(source_test_file),
    "_test_file.exe_extracted/_test_file.pyc",
])
print("FINISH: CONVERT PYC TO PY")
print()

print(f"Content {source_test_file.name}:")
print(source_test_file.read_text("utf-8"))
