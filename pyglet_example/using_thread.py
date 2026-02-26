#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from threading import Thread

# pip install pyglet
import pyglet


def play_song() -> None:
    song = pyglet.media.load("speak.mp3")
    song.play()
    pyglet.app.run()


thread = Thread(target=play_song)
thread.start()

print("Song...")
