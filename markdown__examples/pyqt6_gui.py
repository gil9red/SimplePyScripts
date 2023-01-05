#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from pathlib import Path

# pip install pyqt6
from PyQt6.QtWidgets import QApplication, QWidget, QTextEdit, QLabel, QSplitter, QVBoxLayout, QTabWidget

# pip install markdown
import markdown

from common import EXAMPLE_MARKDOWN


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(Path(__file__).stem)

        self.edit_markdown = QTextEdit()
        self.edit_markdown.textChanged.connect(self._on_input_text_markdown)

        self.edit_result_qt = QTextEdit()
        self.edit_result_qt.setReadOnly(True)

        self.edit_result_markdown = QTextEdit()
        self.edit_result_markdown.setReadOnly(True)

        left_side_layout = QVBoxLayout()
        left_side_layout.addWidget(QLabel('Markdown:'))
        left_side_layout.addWidget(self.edit_markdown)

        left_side = QWidget()
        left_side.setLayout(left_side_layout)

        tab_result = QTabWidget()
        tab_result.addTab(self.edit_result_qt, 'Result (Qt)')
        tab_result.addTab(self.edit_result_markdown, 'Result (markdown)')

        splitter = QSplitter()
        splitter.addWidget(left_side)
        splitter.addWidget(tab_result)

        main_layout = QVBoxLayout()
        main_layout.addWidget(splitter)

        self.setLayout(main_layout)

    def _on_input_text_markdown(self):
        self.edit_result_qt.setMarkdown(self.edit_markdown.toPlainText())

        html = markdown.markdown(self.edit_markdown.toPlainText())
        self.edit_result_markdown.setHtml(html)


if __name__ == '__main__':
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    mw.edit_markdown.setPlainText(EXAMPLE_MARKDOWN)

    app.exec()
