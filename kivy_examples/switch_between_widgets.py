#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


class ScreenMain(Screen):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        box_layout = BoxLayout(orientation="vertical", spacing=5, padding=[10])

        button_new_pasword = Button(
            text="New Pasword",
            background_color=[0, 1.5, 3, 1],
            size_hint=[1, 0.1],
            on_press=self._on_press_button_new_pasword,
        )

        box_layout.add_widget(button_new_pasword)
        self.add_widget(box_layout)

    def _on_press_button_new_pasword(self, *args) -> None:
        self.manager.transition.direction = "left"
        self.manager.current = "len_password"


class ScreenLenPassword(Screen):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        box_layout = BoxLayout(orientation="vertical", spacing=5, padding=[10])

        button_new_pasword = Button(
            text="Return",
            background_color=[2, 1.5, 3, 1],
            size_hint=[1, 0.1],
            on_press=self._on_press_button_new_pasword,
        )

        box_layout.add_widget(button_new_pasword)
        self.add_widget(box_layout)

    def _on_press_button_new_pasword(self, *args) -> None:
        self.manager.transition.direction = "right"
        self.manager.current = "main_screen"


class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(ScreenMain(name="main_screen"))
        sm.add_widget(ScreenLenPassword(name="len_password"))

        return sm


if __name__ == "__main__":
    MainApp().run()
