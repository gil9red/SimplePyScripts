#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://habrahabr.ru/post/346146/


import time

# pip install pyautogui
import pyautogui

from graphics import GraphWin, Circle, Point, Entry, color_rgb


win = GraphWin(
    "pipetka", 200, 200, autoflush=True
)  # создаем графическую форму размером 200х200 и элементы на ней
x, y = pyautogui.position()  # получаем в x, y координаты мыши
r, g, b = pyautogui.pixel(x, y)  # получаем в r, g, b цвет

ColorDot = Circle(Point(100, 100), 25)  # создаем точку, отображающую цвет

# Устанавливает ей заливку из ранее полученных цветов
ColorDot.setFill(color_rgb(r, g, b))
ColorDot.draw(win)  # рисуем на форме win

RGBtext = Entry(Point(win.getWidth() / 2, 25), 10)  # создаем RGB вывод
RGBtext.draw(win)  # рисуем на форме win

RGBstring = Entry(Point(win.getWidth() / 2, 45), 10)  # создаем вывод цвета в web стиле
RGBstring.draw(win)  # рисуем на форме win

Coordstring = Entry(Point(win.getWidth() / 2, 185), 10)  # создаем отображение координат
Coordstring.draw(win)  # рисуем на форме win

while True:  # цикл перереисовки формы
    time.sleep(0.1)  # задержка в 0.1 с, чтобы питон не сходил с ума

    x, y = pyautogui.position()  # получаем в x, y координаты мыши
    r, g, b = pyautogui.pixel(x, y)  # получаем в r, g, b цвет
    ColorDot.setFill(color_rgb(r, g, b))  # Обновляем цвет
    RGBtext.setText(pyautogui.pixel(x, y))  # Обновляем RGB
    RGBstring.setText(color_rgb(r, g, b))  # Обновляем web цвет
    Coordstring.setText("{} x {}".format(x, y))  # Обновляем координаты

    if win.isClosed():
        break

    win.flush()  # Даем команду на перерисовку формы
