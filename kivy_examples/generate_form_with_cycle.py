#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label


class MyWidget(GridLayout):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.cols = 1
        self.spacing = 10
        self.padding = 10

        label_list = ["Собака", "Сосед", "Кот", "Биткоин"]
        for i, title in enumerate(label_list):
            label = Label(text=title)
            label.id = "id:" + str(i)

            self.add_widget(label)


class MyApp(App):
    def build(self):
        return MyWidget()


if __name__ == "__main__":
    MyApp().run()
