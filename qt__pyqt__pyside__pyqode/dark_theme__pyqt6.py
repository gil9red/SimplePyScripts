#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)

# NOTE: -platform windows:darkmode=mode
#       Available options for the Windows dark mode platform integration in Qt6:
#           windows:darkmode=0 -> Complete disable. Application stays light, ignoring OS theme.
#           windows:darkmode=1 -> Partial integration. Darkens only the title bar and window borders.
#           windows:darkmode=2 -> Full integration. Darkens the title bar and all client area widgets.
#           windows:darkmode=3 -> Forced dark mode. Application is always dark, ignoring OS settings (Qt 6.8+).
#       Theme behavior on other Operating Systems in Qt6:
#           macOS -> Handled natively by the OS via QStyle. Automatically switches between
#               Light/Dark appearance based on System Settings without extra arguments.
#           Linux -> Depends on the desktop environment (KDE/GNOME) and active QPA platform theme.
#               Uses environment variables like QT_QPA_PLATFORMTHEME=qt6ct or adwaita.
#
# Example:
# sys.argv += ["-platform", "windows:darkmode=0"]


class MainWindow(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        layout_buttons = QHBoxLayout()
        layout_buttons.addWidget(
            QPushButton(
                "Dark",
                clicked=lambda: QApplication.styleHints().setColorScheme(
                    Qt.ColorScheme.Dark
                ),
            )
        )
        layout_buttons.addWidget(
            QPushButton(
                "Light",
                clicked=lambda: QApplication.styleHints().setColorScheme(
                    Qt.ColorScheme.Light
                ),
            )
        )
        layout_buttons.addWidget(
            QPushButton(
                "Default",
                clicked=lambda: QApplication.styleHints().setColorScheme(
                    Qt.ColorScheme.Unknown
                ),
            )
        )

        self.label = QLabel()

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addLayout(layout_buttons)

        self.setLayout(layout)

        QApplication.styleHints().colorSchemeChanged.connect(self.update_states)

        self.update_states()

    def update_states(self) -> None:
        self.label.setText(f"Theme: {QApplication.styleHints().colorScheme().name}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    mw = MainWindow()
    mw.show()

    app.exec()
