#!/usr/bin/env python3
# -*- coding: utf-8 -*-


if __name__ == "__main__":
    import sys

    from PySide.QtGui import QApplication, QMainWindow

    from pyqode.core import api
    from pyqode.core import modes

    app = QApplication(sys.argv)

    editor = api.CodeEdit()

    # Добавление модов: подсветка кода, подсветка текущей строки и
    # добавление/удаление отступов используя Tab/Shift+Tab
    editor.modes.append(modes.PygmentsSyntaxHighlighter(editor.document()))
    editor.modes.append(modes.CaretLineHighlighterMode())
    editor.modes.append(modes.IndenterMode())

    editor.setPlainText(open(__file__, encoding="utf-8").read(), None, None)

    mw = QMainWindow()
    mw.setWindowTitle("pyqode")
    mw.setCentralWidget(editor)
    mw.show()

    sys.exit(app.exec_())
