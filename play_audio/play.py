#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
import sys

import play_audio


if __name__ == "__main__":
    if len(sys.argv) > 1:
        play_audio.play(sys.argv[1])
    else:
        file_name = os.path.basename(sys.argv[0])
        print("usage: {} [-h] audio_file_name".format(file_name))
