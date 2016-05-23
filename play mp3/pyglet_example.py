#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import pyglet
# pyglet.lib.load_library('avbin')

song = pyglet.media.load(r'speak.mp3')
song.play()
pyglet.app.run()
