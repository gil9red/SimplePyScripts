#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidgetItem, QListWidget, QWidget, QVBoxLayout, QToolBar


class AdvancedListWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.list_widget = QListWidget()
        self.list_widget.itemSelectionChanged.connect(self._update_states)

        tool_bar = QToolBar()
        self.action_append = tool_bar.addAction("➕", self._append)
        self.action_remove = tool_bar.addAction("➖", self._remove)
        self.action_move_up = tool_bar.addAction("🔼", self._move_up)
        self.action_move_down = tool_bar.addAction("🔽", self._move_down)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(tool_bar)
        main_layout.addWidget(self.list_widget)

        self._update_states()

    def _update_states(self):
        current_row: int = self.list_widget.currentRow()

        is_selected: bool = current_row != -1
        self.action_remove.setVisible(is_selected)

        self.action_move_up.setVisible(is_selected and current_row > 0)
        self.action_move_down.setVisible(is_selected and current_row < self.count() - 1)

    def _append(self):
        item = self.append("New item")

        self.list_widget.setCurrentItem(item)
        self.list_widget.editItem(item)

    def _remove(self):
        current_row: int = self.list_widget.currentRow()
        if current_row == -1:
            return

        self.list_widget.takeItem(current_row)

    def _move_item(self, from_row: int, to_row: int):
        item = self.list_widget.takeItem(from_row)
        self.list_widget.insertItem(to_row, item)
        self.list_widget.setCurrentItem(item)

    def _move_up(self):
        current_row: int = self.list_widget.currentRow()
        if current_row < 1:
            return

        self._move_item(current_row, current_row - 1)

    def _move_down(self):
        current_row: int = self.list_widget.currentRow()
        if current_row != -1 and current_row >= self.count() - 1:
            return

        self._move_item(current_row, current_row + 1)

    def append(self, text: str) -> QListWidgetItem:
        item = QListWidgetItem(text)
        item.setFlags(item.flags() | Qt.ItemIsEditable)

        self.list_widget.addItem(item)

        return item

    def append_all(self, items: list[str]):
        for text in items:
            self.append(text)

    def clear(self):
        return self.list_widget.clear()

    def count(self) -> int:
        return self.list_widget.count()

    def get(self, i: int) -> str:
        return self.list_widget.item(i).text()

    def items(self) -> list[str]:
        return [self.get(i) for i in range(self.count())]


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])

    mw = AdvancedListWidget()
    mw.append_all(
        [
            "FOO",
            "BAR",
            "GO",
            "ABC",
            "123",
            "!!!",
        ]
    )
    mw.show()

    app.exec()
