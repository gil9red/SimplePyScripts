#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PySide.QtGui import *
from PySide.QtCore import *

from add_student_dialog import AddStudentDialog


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Students")

        self.toolBar = QToolBar("General")
        self.addToolBar(self.toolBar)

        self.action_add = self.toolBar.addAction("Add")
        self.action_add.triggered.connect(self.add)

        self.action_remove = self.toolBar.addAction("Remove")
        self.action_remove.triggered.connect(self.remove)

        self.table = QTableWidget()
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)

        headers = ["Name", "Group"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        self.setCentralWidget(self.table)

    def add(self):
        dialog = AddStudentDialog()
        if dialog.exec():
            student = dialog.student
            if student is None:
                raise Exception("student is None")

            row = self.table.rowCount()
            self.table.setRowCount(row + 1)

            self.table.setItem(row, 0, QTableWidgetItem(student.name))
            self.table.setItem(row, 1, QTableWidgetItem(student.group))

    def remove(self):
        row = self.table.currentRow()
        if row != -1:
            self.table.removeRow(row)
