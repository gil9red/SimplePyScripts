#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os

from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem


KV = '''
ScrollView:
    MDList:
        id: container
'''


class Test(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        for i in os.listdir(path='.'):
            self.root.ids.container.add_widget(
                OneLineListItem(text=i, on_release=lambda item, i=i: print(i))
            )


if __name__ == '__main__':
    Test().run()
