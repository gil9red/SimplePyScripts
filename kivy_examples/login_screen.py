#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup


class LoginScreen(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 2
        self.spacing = 10
        self.padding = 10

        self.add_widget(Label(text="User Name"))
        self.username = TextInput(multiline=False)
        self.username.text = "admin"
        self.add_widget(self.username)

        self.add_widget(Label(text="password"))
        self.password = TextInput(password=True, multiline=False)
        self.password.text = "admin"
        self.add_widget(self.password)

        self.add_widget(Button(text="Ok", on_press=self.check))

    def check(self, button):
        print("auth called")

        message = "Success!" if self.username.text == "admin" else "Need admin!"

        popup = Popup(
            title="Info",
            content=Label(text=message),
            size=(100, 100),
            size_hint=(0.3, 0.3),
            auto_dismiss=True,
        )

        popup.open()


class MyLoginScreenApp(App):
    def build(self):
        return LoginScreen()


if __name__ == "__main__":
    MyLoginScreenApp().run()
