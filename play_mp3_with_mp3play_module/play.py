#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# https://pypi.python.org/pypi/mp3play/


def play(filename):
    import mp3play
    clip = mp3play.load(filename)
    clip.play()

    import time
    time.sleep(min(30, clip.seconds()))
    clip.stop()
