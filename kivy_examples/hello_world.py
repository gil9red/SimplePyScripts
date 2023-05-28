#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Install kivy:
# python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew
# python -m pip install kivy


from kivy.app import App
from kivy.uix.label import Label


class MyApp(App):
    def build(self):
        return Label(text="Hello world")


if __name__ == "__main__":
    MyApp().run()
