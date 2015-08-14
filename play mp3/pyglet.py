#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import pyglet
pyglet.lib.load_library('avbin')

song = pyglet.media.load(r'C:\Users\ipetrash\Music\Эпоха – Ценой великих жертв.mp3')
song.play()
pyglet.app.run()
