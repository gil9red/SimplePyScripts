#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
from pathlib import Path

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
)
from PyQt5.QtCore import Qt

from db import Dossier, shorten


def _get_field_widget(title: str, widget: QWidget) -> QWidget:
    layout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(QLabel(title))
    layout.addWidget(widget)

    widget = QWidget()
    widget.setLayout(layout)

    return widget


def _get_line_edit(text: str) -> QLineEdit:
    line_edit = QLineEdit()
    line_edit.setReadOnly(True)
    line_edit.setText(text)
    line_edit.setStyleSheet(
        """
        QLineEdit {
            border: 0;
            background: transparent;
        }
    """
    )

    return line_edit


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/0a066058edc26164910bc00fd35d7815a1eed06a/parse_jira_Assigned_Open_Issues_per_Project/gui.py#L48
def get_table_widget(header_labels: list) -> QTableWidget:
    table = QTableWidget()
    table.setAlternatingRowColors(True)
    table.setEditTriggers(QTableWidget.NoEditTriggers)
    table.setSelectionBehavior(QTableWidget.SelectRows)
    table.setSelectionMode(QTableWidget.SingleSelection)
    table.setColumnCount(len(header_labels))
    table.setHorizontalHeaderLabels(header_labels)
    table.horizontalHeader().setStretchLastSection(True)
    return table


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.filter_le = QLineEdit()
        self.filter_le.setPlaceholderText("Enter for search regexp...")
        self.filter_le.textEdited.connect(self.fill)

        self.table_dossier = get_table_widget(["TITLE"])
        self.table_dossier.itemClicked.connect(self._on_table_dossier_item_clicked)

        self.table_items = get_table_widget(["CONTENT"])
        self.table_items.itemClicked.connect(self._on_table_items_item_clicked)

        self.question_te = QTextEdit()
        self.answer_te = QTextEdit()

        self.dossier_title = _get_line_edit("-")
        self.dossier_url = _get_line_edit("-")
        self.dossier_date = QLabel("-")
        self.dossier_total_items = QLabel("-")

        central_content_widget = QWidget()
        central_content_widget.setLayout(QGridLayout())
        central_content_widget.layout().addWidget(QLabel("Title:"), 0, 0)
        central_content_widget.layout().addWidget(self.dossier_title, 0, 1)
        central_content_widget.layout().addWidget(QLabel("Url:"), 1, 0)
        central_content_widget.layout().addWidget(self.dossier_url, 1, 1)
        central_content_widget.layout().addWidget(QLabel("Date:"), 2, 0)
        central_content_widget.layout().addWidget(self.dossier_date, 2, 1)
        central_content_widget.layout().addWidget(QLabel("Total items:"), 3, 0)
        central_content_widget.layout().addWidget(self.dossier_total_items, 3, 1)
        central_content_widget.layout().addWidget(self.table_items, 4, 0, 1, 2)

        right_splitter = QSplitter(Qt.Vertical)
        right_splitter.addWidget(_get_field_widget("Question:", self.question_te))
        right_splitter.addWidget(_get_field_widget("Answer:", self.answer_te))

        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.addWidget(self.table_dossier)
        main_splitter.addWidget(central_content_widget)
        main_splitter.addWidget(right_splitter)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.filter_le)
        main_layout.addWidget(main_splitter)

        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(main_layout)

    def _get_search_pattern(self):
        search_text = self.filter_le.text()
        try:
            return re.compile(search_text, flags=re.IGNORECASE)
        except:
            pass

    def fill(self):
        # Удаление строк таблицы
        while self.table_dossier.rowCount():
            self.table_dossier.removeRow(0)

        items = Dossier.select()

        search_text = self.filter_le.text()
        pattern = self._get_search_pattern()
        if search_text and pattern:
            new_items = []
            for dossier in items:
                found = False
                for x in dossier.items:
                    if pattern.search(x.question_text) or pattern.search(x.question_text):
                        found = True
                        break
                if found:
                    new_items.append(dossier)

            items = new_items

        for i, dossier in enumerate(items):
            self.table_dossier.setRowCount(self.table_dossier.rowCount() + 1)

            item = QTableWidgetItem(dossier.title)
            item.setData(Qt.UserRole, dossier)
            self.table_dossier.setItem(i, 0, item)

        self.table_dossier.setCurrentCell(0, 0)
        self._on_table_dossier_item_clicked()

    def _on_table_dossier_item_clicked(self):
        # Удаление строк таблицы
        while self.table_items.rowCount():
            self.table_items.removeRow(0)

        self.question_te.clear()
        self.answer_te.clear()

        item = self.table_dossier.currentItem()
        if not item:
            return

        dossier = item.data(Qt.UserRole)

        self.dossier_title.setText(dossier.title)
        self.dossier_url.setText(dossier.url)
        self.dossier_date.setText(str(dossier.date))
        self.dossier_total_items.setText(str(len(dossier.items)))

        items = dossier.items

        search_text = self.filter_le.text()
        pattern = self._get_search_pattern()
        if search_text and pattern:
            items = [
                x
                for x in items
                if pattern.search(x.question_text) or pattern.search(x.answer_text)
            ]

        for i, question_answer_pairs in enumerate(items):
            self.table_items.setRowCount(self.table_items.rowCount() + 1)

            question_text = question_answer_pairs.question_text
            answer_text = question_answer_pairs.answer_text
            title = shorten(question_text) + " | " + shorten(answer_text)

            item = QTableWidgetItem(title)
            item.setData(Qt.UserRole, question_answer_pairs)
            self.table_items.setItem(i, 0, item)

        self.table_items.setCurrentCell(0, 0)
        self._on_table_items_item_clicked()

    def _on_table_items_item_clicked(self):
        item = self.table_items.currentItem()
        if not item:
            return

        question_answer_pairs = item.data(Qt.UserRole)
        question_text = question_answer_pairs.question_text
        answer_text = question_answer_pairs.answer_text

        search_text = self.filter_le.text()
        pattern = self._get_search_pattern()
        if search_text and pattern:
            question_text = pattern.sub(lambda m: f"<b>{m.group()}</b>", question_text)
            answer_text = pattern.sub(lambda m: f"<b>{m.group()}</b>", answer_text)

        self.question_te.setText(question_text)
        self.answer_te.setText(answer_text)


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.setWindowTitle(Path(__file__).resolve().parent.name)
    mw.resize(1600, 800)
    mw.show()

    mw.fill()

    app.exec()
