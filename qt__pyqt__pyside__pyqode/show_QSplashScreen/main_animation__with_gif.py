#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'

from PyQt5.QtWidgets import QSplashScreen
from PyQt5.QtGui import QMovie, QMouseEvent


class GifSplashScreen(QSplashScreen):
    def __init__(self, file_name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._old_pos = None

        self.movie = QMovie(file_name, parent=self)
        self.movie.frameChanged.connect(self._on_frame_changed)
        self.movie.start()

    def _on_frame_changed(self, _):
        self.setPixmap(self.movie.currentPixmap())

    def finish(self, widget):
        super().finish(widget)

        self.movie.stop()

    def mousePressEvent(self, event: QMouseEvent):
        """
        Переопределенный метод, используется, чтобы при клике окно не скрывалось
        """
        # https://code.woboq.org/qt5/qtbase/src/widgets/widgets/qsplashscreen.cpp.html#_ZN13QSplashScreen15mousePressEventEP11QMouseEvent


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import Qt

    app = QApplication(sys.argv)

    # SOURCE: https://codemyui.com/git-kraken-inspired-rotate-loading-animation/
    splash = GifSplashScreen('rotate-pulsating-loading-animation.gif')
    splash.show()

    from _test_widget import MainWindow

    splash.showMessage('Ожидание создания интерфейса', Qt.AlignHCenter | Qt.AlignBottom, Qt.white)
    w = MainWindow()

    splash.showMessage('Ожидание загрузки данных', Qt.AlignHCenter | Qt.AlignBottom, Qt.white)
    w.do_load()

    w.show()

    splash.finish(w)

    sys.exit(app.exec())
