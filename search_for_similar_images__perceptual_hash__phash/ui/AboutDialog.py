#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QDialog, QTextBrowser, QDialogButtonBox, QVBoxLayout


class AboutDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setWindowTitle("About")

        text_browser = QTextBrowser()
        text_browser.setOpenExternalLinks(True)
        text_browser.setStyleSheet(
            """
            QTextBrowser {
                border: 0;
                background: transparent;
            }
            """
        )
        text_browser.setHtml(
            """
            <div>
                Icons made by 
                <a href="https://icon54.com/" title="Pixel perfect">Pixel perfect</a>,  
                <a href="https://www.flaticon.com/authors/those-icons" title="Those Icons">Those Icons</a>, 
                <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a>
                from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>, 
            </div>
            """
        )

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(text_browser)
        layout.addWidget(button_box)

        self.setLayout(layout)
