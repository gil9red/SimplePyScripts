__author__ = "ipetrash"


from PySide.QtGui import *


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.editor = QTextEdit()
        self.setCentralWidget(self.editor)
        self.setMenuBar(QMenuBar())

        file_menu = self.menuBar().addMenu("Файл")
        file_menu.addAction("Сохранить как...", self.slot_save_as)
        file_menu.addSeparator()
        file_menu.addAction("Выход", self.close)

        self.edit_menu = self.menuBar().addMenu("Правка")
        self.edit_menu.aboutToShow.connect(self.update_edit_menu)

    def update_edit_menu(self) -> None:
        self.edit_menu.clear()
        actions = self.editor.createStandardContextMenu().actions()
        self.edit_menu.addActions(actions)

    def slot_save_as(self) -> None:
        file_name = QFileDialog.getSaveFileName()[0]
        if file_name:
            with open(file_name, "w") as f:
                f.write(self.editor.toPlainText())


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setApplicationName("myWindow")

    w = MainWindow()
    w.show()

    sys.exit(app.exec_())
