#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import traceback


from PyQt5 import Qt

from lxml import etree

# pip install cssselect
from lxml.cssselect import CSSSelector


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    import traceback
    text += ''.join(traceback.format_tb(tb))

    print(text)
    Qt.QMessageBox.critical(None, 'Error', text)
    quit()


import sys
sys.excepthook = log_uncaught_exceptions


class MainWindow(Qt.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('xml_html__xpath__css_selector__gui')

        self.le_xpath_css = Qt.QLineEdit()

        self.rb_xpath = Qt.QRadioButton('XPath')
        self.rb_css_selector = Qt.QRadioButton('CSS selector')
        self.rb_css_selector.setChecked(True)

        self.text_edit_input = Qt.QPlainTextEdit()
        self.text_edit_output = Qt.QPlainTextEdit()

        self.label_error = Qt.QLabel()
        self.label_error.setStyleSheet("QLabel { color : red; }")
        self.label_error.setTextInteractionFlags(Qt.Qt.TextSelectableByMouse)
        self.label_error.setSizePolicy(Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Preferred)

        self.button_detail_error = Qt.QPushButton('...')
        self.button_detail_error.setFixedSize(20, 20)
        self.button_detail_error.setToolTip('Detail error')
        self.button_detail_error.hide()

        self.last_error_message = None
        self.last_detail_error_message = None

        self.le_xpath_css.textEdited.connect(self.on_process)
        self.rb_xpath.clicked.connect(self.on_process)
        self.rb_css_selector.clicked.connect(self.on_process)
        self.text_edit_input.textChanged.connect(self.on_process)
        self.button_detail_error.clicked.connect(self.show_detail_error_message)

        splitter = Qt.QSplitter()
        splitter.setSizePolicy(Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Expanding)
        splitter.addWidget(self.text_edit_input)
        splitter.addWidget(self.text_edit_output)

        layout_xpath_css = Qt.QHBoxLayout()
        layout_xpath_css.addWidget(self.le_xpath_css)
        layout_xpath_css.addWidget(self.rb_xpath)
        layout_xpath_css.addWidget(self.rb_css_selector)

        layout = Qt.QVBoxLayout()
        layout.addLayout(layout_xpath_css)
        layout.addWidget(splitter)

        layout_error = Qt.QHBoxLayout()
        layout_error.addWidget(self.label_error)
        layout_error.addWidget(self.button_detail_error)

        layout.addLayout(layout_error)

        self.setLayout(layout)

    def on_process(self):
        self.text_edit_output.clear()
        self.label_error.clear()
        self.button_detail_error.hide()

        self.last_error_message = None
        self.last_detail_error_message = None

        try:
            text = self.text_edit_input.toPlainText()
            if not text or not self.le_xpath_css.text():
                return

            search_text = self.le_xpath_css.text()

            root = etree.fromstring(text)

            if self.rb_xpath.isChecked():
                result = root.xpath(search_text)
            else:
                selector = CSSSelector(search_text)
                result = selector(root)

            print(len(result), result)

            def to_str(x):
                try:
                    return etree.tounicode(x, method='html')
                except:
                    return x

            result = map(to_str, result)
            output = '\n'.join('{}. {}'.format(i, x) for i, x in enumerate(result, 1))
            self.text_edit_output.setPlainText(output)

        except Exception as e:
            # # Выводим ошибку в консоль
            # traceback.print_exc()

            # Сохраняем в переменную
            tb = traceback.format_exc()

            self.last_error_message = str(e)
            self.last_detail_error_message = str(tb)
            self.button_detail_error.show()

            self.label_error.setText('Error: ' + self.last_error_message)

    def show_detail_error_message(self):
        message = self.last_error_message + '\n\n' + self.last_detail_error_message

        mb = Qt.QErrorMessage()
        mb.setWindowTitle('Error')
        # Сообщение ошибки содержит отступы, символы-переходы на следующую строку,
        # которые поломаются при вставке через QErrorMessage.showMessage, и нет возможности
        # выбрать тип текста, то делаем такой хак.
        mb.findChild(Qt.QTextEdit).setPlainText(message)

        mb.exec_()


if __name__ == '__main__':
    app = Qt.QApplication([])

    mw = MainWindow()
    mw.resize(650, 500)
    mw.show()

    # For example
    mw.text_edit_input.setPlainText('''\
<Recipe name="хлеб" preptime="5min" cooktime="180min">
   <Title>Простой хлеб</Title>
   <Composition>
      <Ingredient amount="3" unit="стакан">Мука</Ingredient>
      <Ingredient amount="0.25" unit="грамм">Дрожжи</Ingredient>
      <Ingredient amount="1.5" unit="стакан">Тёплая вода</Ingredient>
   </Composition>
</Recipe>
    ''')
    # //Ingredient[@amount=0.25]
    mw.le_xpath_css.setText("Ingredient[amount='0.25']")
    mw.on_process()

    app.exec_()
