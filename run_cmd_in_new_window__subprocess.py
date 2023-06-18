#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import subprocess


subprocess.run(["start", "cmd.exe", "@cmd", "/k", "ipconfig"], shell=True)
