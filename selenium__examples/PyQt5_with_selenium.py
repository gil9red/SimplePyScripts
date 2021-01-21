#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from urllib.parse import urljoin
import time

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QHBoxLayout, QPushButton, QTextBrowser
)
from PyQt5.QtCore import QThread, pyqtSignal

# pip install selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options


URL = 'https://ru.stackoverflow.com'


class StackOverFlowBotThread(QThread):
    about_search_result = pyqtSignal(str, str)
    about_change_title = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        options = Options()
        # options.add_argument('--headless')

        self.driver = webdriver.Firefox(options=options)
        self.driver.implicitly_wait(10)

        self._search = None

    def search(self, text: str):
        self._search = text

    def run(self):
        self.driver.get(URL)
        print(f'Title: "{self.driver.title}"')
        self.about_change_title.emit(self.driver.title)

        try:
            # Чтобы поток не завершился
            while self.driver:
                if self._search:
                    search_el = self.driver.find_element_by_css_selector('#search .s-input__search')
                    search_el.clear()
                    search_el.send_keys(self._search + Keys.RETURN)

                    # Даем время прогрузиться результату
                    time.sleep(1)
                    self.about_change_title.emit(self.driver.title)

                    for result_el in self.driver.find_elements_by_css_selector('.result-link a[href]'):
                        title = result_el.text.strip()
                        url = urljoin(URL, result_el.get_attribute('href'))
                        self.about_search_result.emit(title, url)

                    # Поиск уже выполнен
                    self._search = None

                time.sleep(0.05)

        finally:
            self.driver.quit()

    def quit(self):
        self.driver.quit()
        self.driver = None

        super().quit()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.search = QLineEdit('gil9red')
        self.search.returnPressed.connect(self.on_search)

        self.button_search = QPushButton('Search')
        self.button_search.clicked.connect(self.on_search)

        self.result = QTextBrowser()
        self.result.setOpenExternalLinks(True)

        self.bot_thread = StackOverFlowBotThread()
        self.bot_thread.about_search_result.connect(self.on_search_result)
        self.bot_thread.about_change_title.connect(self.setWindowTitle)
        self.bot_thread.start()

        layout_search = QHBoxLayout()
        layout_search.addWidget(self.search)
        layout_search.addWidget(self.button_search)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout_search)
        main_layout.addWidget(self.result)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def on_search(self):
        self.result.clear()

        text = self.search.text()
        self.bot_thread.search(text)

    def on_search_result(self, title, url):
        self.result.append(f'<a href="{url}">{title}</a>')

    def closeEvent(self, event):
        self.bot_thread.quit()


if __name__ == '__main__':
    app = QApplication([])

    mw = MainWindow()
    mw.resize(800, 600)
    mw.show()

    app.exec()
