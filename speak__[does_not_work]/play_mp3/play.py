#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def play(file_name) -> None:
    import pyglet
    import os
    dll_file_name = os.path.join(os.path.dirname(__file__), 'avbin')
    pyglet.lib.load_library(dll_file_name)

    player = pyglet.media.Player()
    source = pyglet.media.load(file_name)
    player.queue(source)

    player.play()

    def update(dt) -> None:
        if not player.playing:
            # Отпишем функцию, иначе при повторном вызове, иначе
            # будет двойной вызов при следующем воспроизведении
            pyglet.clock.unschedule(update)
            pyglet.app.exit()

    # Every 500 ms / 0.5 sec
    pyglet.clock.schedule_interval(update, 0.5)
    pyglet.app.run()


if __name__ == '__main__':
    play('speak_male.mp3')
