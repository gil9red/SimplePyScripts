#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5 import Qt


class Widget(Qt.QWidget):
    def __init__(self):
        super().__init__()

        self.indicator = Qt.QLabel()
        self.indicator.hide()
        self.indicator.setFixedSize(32, 32)
        self.indicator.setScaledContents(True)
        self.indicator.setPixmap(Qt.QPixmap("light-bulb-icon_34400.png"))

        self.line_edit = Qt.QLineEdit()
        self.line_edit.textEdited.connect(self._on_text_edited)

        self.status_bar = Qt.QStatusBar()
        self.status_bar.addPermanentWidget(self.indicator)
        self.status_bar.setSizeGripEnabled(False)  # Убираем снизу-справа уголок

        main_layout = Qt.QVBoxLayout()
        # Сверху, слева и справа отступ 5, внизу его нет
        main_layout.setContentsMargins(
            5, 5, 5, 0
        )
        main_layout.addWidget(self.line_edit)
        main_layout.addStretch()
        main_layout.addWidget(self.status_bar)

        self.setLayout(main_layout)

    def _on_text_edited(self, text):
        # Показываем сообщение на 2 секунды
        self.status_bar.showMessage(text, msecs=2000)

        # Показываем лампочку
        self.indicator.show()

        # Через 2 секунды лампочка исчезнетв
        Qt.QTimer.singleShot(2000, self.indicator.hide)


if __name__ == "__main__":
    app = Qt.QApplication([])

    w = Widget()
    w.show()

    app.exec()
