#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5 import Qt


class Example(Qt.QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Hi")

        self.text_edit = Qt.QTextEdit()
        self.setCentralWidget(self.text_edit)

        menu = self.menuBar().addMenu("File")
        save_file_action = menu.addAction("Save As ...")
        save_file_action.triggered.connect(self.save_as)

    def save_as(self) -> None:
        file_name, ok = Qt.QFileDialog.getSaveFileName(self)
        if not ok:
            return

        with open(file_name, "w", encoding="utf-8") as f:
            text = self.text_edit.toPlainText()
            f.write(text)


if __name__ == "__main__":
    import sys

    app = Qt.QApplication(sys.argv)

    example = Example()
    example.setGeometry(300, 300, 300, 300)
    example.show()

    app.exec()
