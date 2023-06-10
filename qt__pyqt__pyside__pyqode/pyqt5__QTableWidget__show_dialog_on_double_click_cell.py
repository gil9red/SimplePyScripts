#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5 import Qt


class MainWindow(Qt.QMainWindow):
    def __init__(self):
        super().__init__()

        self.table = Qt.QTableWidget()
        self.table.setRowCount(3)
        self.table.setColumnCount(2)
        self.table.itemDoubleClicked.connect(self.on_cell_item_clicked)

        rows = ["Vasya", "Petya", "Masha"]

        for i, value in enumerate(rows):
            self.table.setItem(i, 0, Qt.QTableWidgetItem(str(i + 1)))
            self.table.setItem(i, 1, Qt.QTableWidgetItem(value))

        layout = Qt.QVBoxLayout()
        layout.addWidget(self.table)
        main_widget = Qt.QWidget()
        main_widget.setLayout(layout)

        self.setCentralWidget(main_widget)

    def on_cell_item_clicked(self, item):
        print(item)

        new_text, ok = Qt.QInputDialog.getText(
            self, "Change Name", "Change Name", text=item.text()
        )
        if ok:
            item.setText(new_text)


if __name__ == "__main__":
    app = Qt.QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
