#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


if __name__ == '__main__':
    try:
        import subprocess
        java_version = subprocess.check_output(['java', '-version'], stderr=subprocess.STDOUT)
        java_version = java_version.decode()

    except:
        java_version = None

    if java_version:
        print(java_version)
