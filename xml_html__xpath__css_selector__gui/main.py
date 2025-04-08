#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import traceback

from PyQt5.QtWidgets import (
    QWidget,
    QLineEdit,
    QRadioButton,
    QLabel,
    QPlainTextEdit,
    QSizePolicy,
    QPushButton,
    QButtonGroup,
    QSplitter,
    QHBoxLayout,
    QVBoxLayout,
    QErrorMessage,
    QTextEdit,
)
from PyQt5.QtCore import Qt

from lxml import etree, html

# pip install cssselect==1.3.0
from lxml.cssselect import CSSSelector


def to_str(el: "Element") -> str:
    try:
        return etree.tostring(el, method="html", encoding="unicode")
    except:
        return str(el)


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    print(text)
    Qt.QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("xml_html__xpath__css_selector__gui")

        self.le_xpath_css = QLineEdit()

        self.rb_xpath = QRadioButton("XPath")
        self.rb_css_selector = QRadioButton("CSS selector")
        self.rb_css_selector.setChecked(True)

        self.text_edit_input = QPlainTextEdit()
        self.text_edit_output = QPlainTextEdit()

        self.label_error = QLabel()
        self.label_error.setStyleSheet("QLabel { color : red; }")
        self.label_error.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label_error.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.button_detail_error = QPushButton("...")
        self.button_detail_error.setFixedSize(20, 20)
        self.button_detail_error.setToolTip("Detail error")
        self.button_detail_error.hide()

        self.last_error_message: str = ""
        self.last_detail_error_message: str = ""

        self.le_xpath_css.textEdited.connect(self.on_process)
        self.rb_xpath.clicked.connect(self.on_process)
        self.rb_css_selector.clicked.connect(self.on_process)
        self.text_edit_input.textChanged.connect(self.on_process)
        self.button_detail_error.clicked.connect(self.show_detail_error_message)

        self.rb_parser_html = QRadioButton("HTML")
        self.rb_parser_html.setChecked(True)
        self.rb_parser_xml = QRadioButton("XML")

        self.button_parser_group = QButtonGroup()
        self.button_parser_group.addButton(self.rb_parser_xml)
        self.button_parser_group.addButton(self.rb_parser_html)

        self.button_parser_group.buttonClicked.connect(self.on_process)

        splitter = QSplitter()
        splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        splitter.addWidget(self.text_edit_input)
        splitter.addWidget(self.text_edit_output)

        layout_xpath_css = QHBoxLayout()
        layout_xpath_css.addWidget(self.le_xpath_css)
        layout_xpath_css.addWidget(self.rb_xpath)
        layout_xpath_css.addWidget(self.rb_css_selector)

        layout = QVBoxLayout()
        layout.addLayout(layout_xpath_css)
        layout.addWidget(splitter)

        layout_input_parser = QHBoxLayout()
        layout_input_parser.addWidget(QLabel("Parser:"))
        layout_input_parser.addWidget(self.rb_parser_html)
        layout_input_parser.addWidget(self.rb_parser_xml)
        layout_input_parser.addStretch()
        layout.addLayout(layout_input_parser)

        layout_error = QHBoxLayout()
        layout_error.addWidget(self.label_error)
        layout_error.addWidget(self.button_detail_error)

        layout.addLayout(layout_error)

        self.setLayout(layout)

    def on_process(self):
        self.text_edit_output.clear()
        self.label_error.clear()
        self.button_detail_error.hide()

        self.last_error_message = ""
        self.last_detail_error_message = ""

        try:
            text = self.text_edit_input.toPlainText()
            if not text or not self.le_xpath_css.text():
                return

            search_text = self.le_xpath_css.text()

            is_html_parser = self.rb_parser_html.isChecked()

            if is_html_parser:
                root = html.fromstring(text)
            else:
                root = etree.fromstring(text)

            if self.rb_xpath.isChecked():
                result = root.xpath(search_text)
            else:
                selector = CSSSelector(
                    search_text,
                    translator="html" if is_html_parser else "xml",
                )
                result = selector(root)

            print(len(result), result)

            result = map(to_str, result)
            output = "\n".join(f"{i}. {x}" for i, x in enumerate(result, 1))
            self.text_edit_output.setPlainText(output)

        except Exception as e:
            # # Выводим ошибку в консоль
            # traceback.print_exc()

            # Сохраняем в переменную
            tb = traceback.format_exc()

            self.last_error_message = str(e)
            self.last_detail_error_message = str(tb)
            self.button_detail_error.show()

            self.label_error.setText("Error: " + self.last_error_message)

    def show_detail_error_message(self):
        message = self.last_error_message + "\n\n" + self.last_detail_error_message

        mb = QErrorMessage()
        mb.setWindowTitle("Error")
        # Сообщение ошибки содержит отступы, символы-переходы на следующую строку,
        # которые поломаются при вставке через QErrorMessage.showMessage, и нет возможности
        # выбрать тип текста, то делаем такой хак.
        mb.findChild(QTextEdit).setPlainText(message)

        mb.exec_()


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])

    mw = MainWindow()
    mw.resize(650, 500)
    mw.show()

    # For example
    mw.text_edit_input.setPlainText(
        """\
<Recipe name="хлеб" preptime="5min" cooktime="180min">
   <Title>Простой хлеб</Title>
   <Composition>
      <Ingredient amount="3" unit="стакан">Мука</Ingredient>
      <Ingredient amount="0.25" unit="грамм">Дрожжи</Ingredient>
      <Ingredient amount="1.5" unit="стакан">Тёплая вода</Ingredient>
   </Composition>
</Recipe>
    """
    )
    # //Ingredient[@amount=0.25]
    mw.le_xpath_css.setText("Ingredient[amount='0.25']")
    mw.on_process()

    app.exec_()
