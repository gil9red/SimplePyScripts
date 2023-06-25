#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import shutil


DIR_NAME = "../extract_directory/dir_1.zip"
OUTPUT = "dir_1"

shutil.unpack_archive(DIR_NAME, OUTPUT)
