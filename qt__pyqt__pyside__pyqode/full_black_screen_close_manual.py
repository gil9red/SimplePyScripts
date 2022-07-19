#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QToolButton, QSizePolicy, QGraphicsOpacityEffect
from PyQt5.QtCore import QPropertyAnimation, QSequentialAnimationGroup


class MainWindow(QWidget):
    def __init__(self, background_color: str = 'black', text_color: str = 'white'):
        super().__init__()

        self.setStyleSheet(f"""
            MainWindow {{
                background-color: {background_color};
            }}
            
            QToolButton {{
                color: {text_color};
                background-color: {background_color};
                border: 1px solid darkgray;
            }}
        """)

        self.button_close = QToolButton()
        self.button_close.setText('ЗАКРЫТЬ')
        self.button_close.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.button_close.setFixedHeight(60)
        self.button_close.clicked.connect(self.close)

        self._add_animations()

        main_layout = QVBoxLayout(self)
        main_layout.addStretch()
        main_layout.addWidget(self.button_close)

    def _add_animations(self):
        self.button_close.setGraphicsEffect(QGraphicsOpacityEffect())

        animation_object = self.button_close.graphicsEffect()
        animation_property = b'opacity'
        duration = 5000
        start_value = 1.0
        end_value = 0.0

        animation1 = QPropertyAnimation(animation_object, animation_property)
        animation1.setDuration(duration)
        animation1.setStartValue(start_value)
        animation1.setEndValue(end_value)

        animation2 = QPropertyAnimation(animation_object, animation_property)
        animation2.setDuration(duration)
        animation2.setStartValue(end_value)
        animation2.setEndValue(start_value)

        self.animation_group = QSequentialAnimationGroup()
        self.animation_group.addAnimation(animation1)
        self.animation_group.addAnimation(animation2)
        self.animation_group.start()


if __name__ == '__main__':
    app = QApplication([])

    mw = MainWindow()
    mw.resize(600, 600)
    # mw.show()
    mw.showFullScreen()

    app.exec()
