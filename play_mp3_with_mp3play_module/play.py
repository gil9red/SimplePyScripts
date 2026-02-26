#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time

# https://pypi.python.org/pypi/mp3play/
import mp3play


def play(filename) -> None:
    clip = mp3play.load(filename)
    clip.play()

    time.sleep(min(30, clip.seconds()))
    clip.stop()


if __name__ == "__main__":
    # TODO: не работает:     print 'Error %s for "%s": %s' % (str(err), txt, buf)
    #                             ^SyntaxError: invalid syntax
    play(r"speak.mp3")
