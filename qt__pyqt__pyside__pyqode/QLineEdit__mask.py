#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://doc.qt.io/qt-5/qlineedit.html#inputMask-prop


from PyQt5.QtWidgets import QApplication, QLineEdit, QWidget, QFormLayout


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.mask_qt = QLineEdit("+7([000])[000]-[0000]")
        self.mask_qt.textEdited.connect(self._on_changed_mask)

        self.test_input = QLineEdit("9991239999")

        layout = QFormLayout()
        layout.addRow("Qt mask:", self.mask_qt)
        layout.addRow("Test", self.test_input)

        self.setLayout(layout)

    def _on_changed_mask(self, mask) -> None:
        text = self.test_input.text()

        self.test_input.setInputMask(mask)
        self.test_input.setText(text)


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
