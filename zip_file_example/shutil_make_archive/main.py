#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import shutil


DIR_NAME = "dir_1"
shutil.make_archive(DIR_NAME, "zip", DIR_NAME)
