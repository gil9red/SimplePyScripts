#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as DT
import os
import sys
import traceback

from pathlib import Path
from timeit import default_timer

# pip install imagehash
import imagehash

from PIL import Image

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QSplitter,
    QDockWidget,
    QToolBar,
    QWidget,
    QVBoxLayout,
    QMessageBox,
    QLabel,
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSettings, QSize

from common import (
    shorten,
    sizeof_fmt,
    IMAGE_HASH_ALGO,
    SETTINGS_FILE_NAME,
    ICON_WIDTH,
    ICON_HEIGHT,
    DIR_IMAGES,
    explore,
)
from db import db_get_all, db_add_image, db_exists, db_create_backup

sys.path.append(r"C:\Users\ipetrash\Projects\SimplePyScripts\qt__pyqt__pyside__pyqode")
from layout_append_line__horizontal_vertical import VerticalLineWidget

from ui.FileListModel import FileListModel
from ui.ListImagesWidget import ListImagesWidget
from ui.FieldsProgressDialog import FieldsProgressDialog
from ui.FlatProgressBar import FlatProgressBar
from ui.IndexingSettingsWidget import IndexingSettingsWidget
from ui.SearchForSimilarSettingsWidget import SearchForSimilarSettingsWidget
from ui.AboutDialog import AboutDialog
from ui.ImageHashDetailsDialog import ImageHashDetailsDialog
from ui.CrossSearchSimilarImagesDialog import CrossSearchSimilarImagesDialog


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = "{}: {}:\n".format(ex_cls.__name__, ex)
    text += "".join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


IMAGE_CACHE = dict()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(str(Path(__file__).parent.name))

        self.image_by_hashes: dict[str, dict] = dict()

        self._fill_ui()

        self._update_states()

    def _fill_menus(self):
        self.menu_file = self.menuBar().addMenu("File")
        action_exit = self.menu_file.addAction("Exit")
        action_exit.triggered.connect(self.close)

        self.menu_toolbars = self.menuBar().addMenu("Toolbars")
        self.menu_docks = self.menuBar().addMenu("Docks")

        self.menu_help = self.menuBar().addMenu("Help")
        action_about_qt = self.menu_help.addAction("About Qt")
        action_about_qt.triggered.connect(QApplication.aboutQt)

        action_about = self.menu_help.addAction("About")
        action_about.triggered.connect(lambda: AboutDialog(self).exec())

    def _fill_toolbars(self):
        # tool_bar_general
        self.tool_bar_general = self.addToolBar("General")

        self.action_fill_images_db = self.tool_bar_general.addAction("Fill with images")
        self.action_fill_images_db.setIcon(QIcon(DIR_IMAGES + "/refresh.svg"))
        self.action_fill_images_db.triggered.connect(self.fill_images_db)

        self.action_start_indexing = self.tool_bar_general.addAction("Start indexing")
        self.action_start_indexing.setIcon(QIcon(DIR_IMAGES + "/index.svg"))
        self.action_start_indexing.triggered.connect(self.start_indexing)

        self.action_search_for_similar = self.tool_bar_general.addAction(
            "Search for similar"
        )
        self.action_search_for_similar.setIcon(QIcon(DIR_IMAGES + "/search.svg"))
        self.action_search_for_similar.triggered.connect(self.start_search_for_similar)

        self.action_cross_search_similar_images = self.tool_bar_general.addAction(
            "Cross search similar images"
        )
        self.action_cross_search_similar_images.setIcon(
            QIcon(DIR_IMAGES + "/search-cross.svg")
        )
        self.action_cross_search_similar_images.triggered.connect(
            self.cross_search_similar_images
        )

        # self.action_scroll_to_origin = self.tool_bar_general.addAction('Scroll to origin')
        # self.action_scroll_to_origin.triggered.connect(self.scroll_to_origin)
        # tool_bar_general

        # tool_bar_indexed_image_control
        self.tool_bar_indexed_image_control = self.addToolBar("Indexed image control")

        self.action_select_indexed_image = (
            self.tool_bar_indexed_image_control.addAction("Select indexed image")
        )
        self.action_select_indexed_image.setIcon(QIcon(DIR_IMAGES + "/image.svg"))
        self.action_select_indexed_image.triggered.connect(self.select_indexed_image)

        self.action_open_indexed_image_directory = (
            self.tool_bar_indexed_image_control.addAction(
                "Open indexed image directory"
            )
        )
        self.action_open_indexed_image_directory.setIcon(
            QIcon(DIR_IMAGES + "/folder.svg")
        )
        self.action_open_indexed_image_directory.triggered.connect(
            self.open_indexed_image_directory
        )

        self.action_run_indexed_image = self.tool_bar_indexed_image_control.addAction(
            "Run indexed image"
        )
        self.action_run_indexed_image.setIcon(QIcon(DIR_IMAGES + "/run_image.svg"))
        self.action_run_indexed_image.triggered.connect(self.run_indexed_image)

        self.action_view_details_indexed_image = (
            self.tool_bar_indexed_image_control.addAction("View details")
        )
        self.action_view_details_indexed_image.setIcon(QIcon(DIR_IMAGES + "/view.svg"))
        self.action_view_details_indexed_image.triggered.connect(
            self.view_details_indexed_image
        )
        # tool_bar_indexed_image_control

        # tool_bar_similar_image_control
        self.tool_bar_similar_image_control = self.addToolBar("Similar image control")

        self.action_select_similar_image = (
            self.tool_bar_similar_image_control.addAction("Select similar image")
        )
        self.action_select_similar_image.setIcon(QIcon(DIR_IMAGES + "/image.svg"))
        self.action_select_similar_image.triggered.connect(self.select_similar_image)

        self.action_open_similar_image_directory = (
            self.tool_bar_similar_image_control.addAction(
                "Open similar image directory"
            )
        )
        self.action_open_similar_image_directory.setIcon(
            QIcon(DIR_IMAGES + "/folder.svg")
        )
        self.action_open_similar_image_directory.triggered.connect(
            self.open_similar_image_directory
        )

        self.action_run_similar_image = self.tool_bar_similar_image_control.addAction(
            "Run similar image"
        )
        self.action_run_similar_image.setIcon(QIcon(DIR_IMAGES + "/run_image.svg"))
        self.action_run_similar_image.triggered.connect(self.run_similar_image)

        self.action_view_details_similar_image = (
            self.tool_bar_similar_image_control.addAction("View details")
        )
        self.action_view_details_similar_image.setIcon(QIcon(DIR_IMAGES + "/view.svg"))
        self.action_view_details_similar_image.triggered.connect(
            self.view_details_similar_image
        )
        # tool_bar_similar_image_control

    def _fill_dockwidgets(self):
        self.indexing_settings = IndexingSettingsWidget()
        indexing_settings_widget_dock_widget = QDockWidget(
            self.indexing_settings.windowTitle()
        )
        indexing_settings_widget_dock_widget.setWidget(self.indexing_settings)
        self.addDockWidget(Qt.RightDockWidgetArea, indexing_settings_widget_dock_widget)

        self.search_for_similar_settings = SearchForSimilarSettingsWidget()
        search_for_similar_settings_dock_widget = QDockWidget(
            self.search_for_similar_settings.windowTitle()
        )
        search_for_similar_settings_dock_widget.setWidget(
            self.search_for_similar_settings
        )
        self.addDockWidget(
            Qt.RightDockWidgetArea, search_for_similar_settings_dock_widget
        )

    def _fill_ui(self):
        self._fill_menus()
        self._fill_toolbars()
        self._fill_dockwidgets()

        self.status_bar_indexed_image = QLabel()
        self.status_bar_similar_image = QLabel()

        self._status_bar_line_sep = VerticalLineWidget()

        # Удаление разделителя между элементами в QStatusBar
        self.statusBar().setStyleSheet("QStatusBar::item { border: none; }")
        self.statusBar().addWidget(self.status_bar_indexed_image)
        self.statusBar().addWidget(self._status_bar_line_sep)
        self.statusBar().addWidget(self.status_bar_similar_image)

        # files
        self.model_files = FileListModel()
        self.model_files.numberPopulated.connect(self._update_states)
        self.search_for_similar_settings.about_mark_matching.connect(
            lambda flag: (
                self.model_files.set_mark_matching(flag),
                self.list_indexed_images_widget.viewport().repaint(),
            )
        )

        self.list_indexed_images_widget = ListImagesWidget(
            ICON_WIDTH, ICON_HEIGHT, IMAGE_CACHE, file_name_index=0
        )
        self.list_indexed_images_widget.clicked.connect(self._update_states)
        self.list_indexed_images_widget.doubleClicked.connect(self.run_indexed_image)
        self.list_indexed_images_widget.setModel(self.model_files)
        # files

        # similar_images
        self.model_similar_images = FileListModel()
        self.model_similar_images.numberPopulated.connect(self._update_states)

        self.list_images_widget_similar = ListImagesWidget(
            ICON_WIDTH, ICON_HEIGHT, IMAGE_CACHE, file_name_index=0
        )
        self.list_images_widget_similar.clicked.connect(self._update_states)
        self.list_images_widget_similar.doubleClicked.connect(self.run_similar_image)
        self.list_images_widget_similar.setModel(self.model_similar_images)
        # similar_images

        # Все действия к прикрепляемым окнам поместим в меню
        for dock in self.findChildren(QDockWidget):
            self.menu_docks.addAction(dock.toggleViewAction())
            dock.setObjectName(dock.widget().__class__.__name__ + "_DockWidget")

        # Все действия к toolbar'ам окнам поместим в меню
        for tool in self.findChildren(QToolBar):
            self.menu_toolbars.addAction(tool.toggleViewAction())

            tool.setObjectName(
                "".join(x.title() for x in tool.windowTitle().strip()) + "_ToolBar"
            )
            tool.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            tool.setIconSize(QSize(32, 32))

        self.progress_bar_list_images_widget = FlatProgressBar()
        self.progress_bar_list_images_widget_similar = FlatProgressBar()

        _top_widget = QWidget()
        _top_widget.setLayout(QVBoxLayout())
        _top_widget.layout().setSpacing(0)
        _top_widget.layout().addWidget(QLabel("Indexed images:"))
        _top_widget.layout().addWidget(self.progress_bar_list_images_widget)
        _top_widget.layout().addWidget(self.list_indexed_images_widget)

        _bottom_widget = QWidget()
        _bottom_widget.setLayout(QVBoxLayout())
        _bottom_widget.layout().setSpacing(0)
        _bottom_widget.layout().addWidget(QLabel("Similar images:"))
        _bottom_widget.layout().addWidget(self.progress_bar_list_images_widget_similar)
        _bottom_widget.layout().addWidget(self.list_images_widget_similar)

        part_splitter_height = max(
            _top_widget.minimumSizeHint().height(),
            _bottom_widget.minimumSizeHint().height(),
        )

        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(_top_widget)
        splitter.addWidget(_bottom_widget)
        splitter.setSizes([part_splitter_height * 2, part_splitter_height / 2])

        self.setCentralWidget(splitter)

    def _update_states(self):
        file_name_indexed = self.list_indexed_images_widget.currentFileName()
        has_index_list_images_widget = bool(file_name_indexed)

        self.action_search_for_similar.setEnabled(has_index_list_images_widget)
        self.action_select_indexed_image.setEnabled(has_index_list_images_widget)
        self.action_open_indexed_image_directory.setEnabled(
            has_index_list_images_widget
        )
        self.action_run_indexed_image.setEnabled(has_index_list_images_widget)
        self.action_view_details_indexed_image.setEnabled(has_index_list_images_widget)
        if has_index_list_images_widget:
            self.status_bar_indexed_image.setText(file_name_indexed)

        file_name_similar = self.list_images_widget_similar.currentFileName()
        has_index_list_images_widget_similar = bool(file_name_similar)
        self.action_select_similar_image.setEnabled(
            has_index_list_images_widget_similar
        )
        self.action_open_similar_image_directory.setEnabled(
            has_index_list_images_widget_similar
        )
        self.action_run_similar_image.setEnabled(has_index_list_images_widget_similar)
        self.action_view_details_similar_image.setEnabled(
            has_index_list_images_widget_similar
        )
        if has_index_list_images_widget_similar:
            self.status_bar_similar_image.setText(file_name_similar)

        # self.action_scroll_to_origin.setEnabled(has_index_list_images_widget_similar)

        self.status_bar_indexed_image.setVisible(has_index_list_images_widget)
        self.status_bar_similar_image.setVisible(has_index_list_images_widget_similar)
        self._status_bar_line_sep.setVisible(
            has_index_list_images_widget and has_index_list_images_widget_similar
        )

        total_model_files = len(self.model_files.fileList)
        if total_model_files == 0:
            # Чтобы не показывался busy-индикатор (бегающая полоска)
            self.progress_bar_list_images_widget.setRange(0, 1)
        else:
            self.progress_bar_list_images_widget.setRange(0, total_model_files)
            self.progress_bar_list_images_widget.setValue(self.model_files.fileCount)

        total_model_similar_images = len(self.model_similar_images.fileList)
        if total_model_similar_images == 0:
            # Чтобы не показывался busy-индикатор (бегающая полоска)
            self.progress_bar_list_images_widget_similar.setRange(0, 1)
        else:
            self.progress_bar_list_images_widget_similar.setRange(
                0, total_model_similar_images
            )
            self.progress_bar_list_images_widget_similar.setValue(
                self.model_similar_images.fileCount
            )

    def fill_images_db(self):
        self.image_by_hashes.clear()

        for row in db_get_all():
            file_name = row["file_name"]
            self.image_by_hashes[file_name] = {
                x: imagehash.hex_to_hash(row[x]) for x in IMAGE_HASH_ALGO
            }

        self.model_files.set_file_list(list(self.image_by_hashes.keys()))

        self._update_states()

    def _get_files(self, path_dir: Path, suffixes: list) -> list:
        # Для составления списка файлов, что нужно обработать
        progress = FieldsProgressDialog(0, 0, "File search...", parent=self)
        progress.show()

        time_start = default_timer()
        start_datetime = DT.datetime.now()
        processed_nums = 0
        file_names = []

        for file in path_dir.rglob("*"):
            QApplication.processEvents()

            if progress.wasCanceled():
                break

            if not file.is_file():
                continue

            processed_nums += 1

            suffix = file.suffix.lstrip(".")
            if suffix.lower() not in suffixes:
                continue

            file_names.append(str(file.resolve()))

            last_file_name = shorten(
                Path(file_names[-1]).name,
            )
            progress.setFields(
                {
                    "Directory path": shorten(str(path_dir), length=50),
                    "Suffixes": ", ".join(suffixes),
                    "Files processed": processed_nums,
                    "Files found": len(file_names),
                    "Elapsed time": str(DT.datetime.now() - start_datetime).rsplit(
                        ".", maxsplit=1
                    )[0],
                    "Last file": last_file_name,
                }
            )

        print(f"Files: {len(file_names)}")

        print(f"\nTotal: {default_timer() - time_start:.2f} secs")
        progress.close()

        return file_names

    def start_indexing(self):
        path_dir = self.indexing_settings.dir_box.getValue()
        path_dir = Path(path_dir).resolve()
        if not path_dir.is_dir():
            QMessageBox.warning(self, "Warning", f"Invalid directory: {path_dir}")
            return

        suffixes_text = self.indexing_settings.line_edit_suffixes.text()
        suffixes = [x.strip() for x in suffixes_text.lower().split(",") if x.strip()]

        file_names = self._get_files(path_dir, suffixes)
        number_file_names = len(file_names)

        print()

        # Для отображения диалога парсинга и заполнения базы
        progress = FieldsProgressDialog(
            0, number_file_names, "Indexing...", parent=self
        )
        progress.show()

        time_start = default_timer()
        start_datetime = DT.datetime.now()
        number = 0

        for i, file_name in enumerate(file_names, 1):
            QApplication.processEvents()

            file_size = sizeof_fmt(os.path.getsize(file_name))
            last_file_name = shorten(
                Path(file_name).name,
            )

            progress.setValue(i)
            progress.setFields(
                {
                    "Progress": f"{i} / {number_file_names}",
                    "Elapsed time": str(DT.datetime.now() - start_datetime).rsplit(
                        ".", maxsplit=1
                    )[0],
                    "File name": f"{last_file_name} ({file_size})",
                }
            )

            if progress.wasCanceled():
                break

            if db_exists(file_name):
                continue

            try:
                time = default_timer()

                db_add_image(file_name)
                number += 1
                print(
                    file_name,
                    f"{default_timer() - time:.2f} secs",
                    sizeof_fmt(os.path.getsize(file_name)),
                )

                progress.setFields(
                    {
                        "Progress": f"{i} / {number_file_names}",
                        "Elapsed time": str(DT.datetime.now() - start_datetime).rsplit(
                            ".", maxsplit=1
                        )[0],
                        "Last file": f"{last_file_name} ({file_size})",
                        "Processing time": f"{default_timer() - time:.2f} secs",
                    }
                )

            except Exception as e:
                print(f'Problem: {e} with "{file_name}"')
                continue

        progress.setValue(number_file_names)

        if number:
            db_create_backup()

        print(f"\nTotal: {default_timer() - time_start:.2f} secs. Added: {number}")

    def start_search_for_similar(self):
        file_name = self.list_indexed_images_widget.currentFileName()
        if not file_name:
            return

        hash_algo = self.search_for_similar_settings.cb_algo.currentText()
        max_score = self.search_for_similar_settings.sb_max_score.value()

        hash_value = self.image_by_hashes[file_name][hash_algo]

        # TODO: Monkey patch. https://github.com/JohannesBuchner/imagehash/issues/112
        if hash_algo == "colorhash":
            hash_value = imagehash.colorhash(Image.open(file_name))

        print(
            f"start_search_for_similar: hash_algo={hash_algo}, max_score={max_score}, "
            f"file_name={file_name}, hash_value={hash_value}"
        )

        number_image_by_hashes = len(self.image_by_hashes)

        # Для составления списка файлов, что нужно обработать
        progress = FieldsProgressDialog(
            0, number_image_by_hashes, "Search for similar...", parent=self
        )
        progress.show()

        time_start = default_timer()
        start_datetime = DT.datetime.now()
        results = []

        for i, (other_file_name, hashes) in enumerate(self.image_by_hashes.items(), 1):
            QApplication.processEvents()

            progress.setValue(i)
            progress.setFields(
                {
                    "File name": file_name,
                    "Hash algo": hash_algo,
                    "Max score": max_score,
                    "Progress": f"{i} / {number_image_by_hashes}",
                    "Elapsed time": str(DT.datetime.now() - start_datetime).rsplit(
                        ".", maxsplit=1
                    )[0],
                }
            )

            if progress.wasCanceled():
                break

            print(i, "/", number_image_by_hashes, other_file_name)
            if other_file_name == file_name:
                continue

            other_hash_value = hashes[hash_algo]

            # TODO: Monkey patch. https://github.com/JohannesBuchner/imagehash/issues/112
            if hash_algo == "colorhash":
                other_hash_value = imagehash.colorhash(Image.open(other_file_name))

            score = hash_value - other_hash_value
            print(
                f"Score: {score:2}. Similar images: {file_name!r} and {other_file_name!r}. "
                f"{hash_value} vs {other_hash_value}"
            )

            # TODO: выяснить максимальные значения для каждого из алгоритмом
            #           думаю, можно ориентироваться на длину хеша
            #           можно в sql посмотреть или в self.image_by_hashes[file_name]
            if score > max_score:
                continue

            # print(f'Score: {score:2}. Similar images: {file_name!r} and {other_file_name!r}. '
            #       f'{hash_value} vs {other_hash_value}')

            results.append(other_file_name)

        progress.setValue(number_image_by_hashes)
        print(f"\nTotal: {default_timer() - time_start:.2f} secs")

        if results:
            self.model_files.set_mark_matching(
                self.search_for_similar_settings.cb_mark_matching.isChecked()
            )
            self.model_files.set_matched_files(file_name, results)

        self.model_similar_images.set_file_list(results)

    def cross_search_similar_images(self):
        hash_algo = self.search_for_similar_settings.cb_algo.currentText()
        max_score = self.search_for_similar_settings.sb_max_score.value()

        d = CrossSearchSimilarImagesDialog(self)
        d.itemDoubleClicked.connect(lambda file_name: explore(file_name, select=False))
        d.start(self.image_by_hashes, hash_algo, max_score)

    # TODO: ...
    # def scroll_to_origin(self):
    #     index_list_images_widget_similar = self.list_images_widget_similar.currentIndex()
    #     if not index_list_images_widget_similar.isValid():
    #         return
    #
    #     file_name = index_list_images_widget_similar.data(Qt.DisplayRole)
    #     index = self.model_similar_images.get_index_by_file_name(file_name, 1)
    #     if not index.isValid():
    #         return
    #
    #     self.list_images_widget_similar.setCurrentIndex(index)
    #     self.list_images_widget_similar.scrollTo(index)

    def select_indexed_image(self):
        file_name = self.list_indexed_images_widget.currentFileName()
        explore(file_name)

    def open_indexed_image_directory(self):
        file_name = self.list_indexed_images_widget.currentFileName()
        explore(Path(file_name).parent, select=False)

    def run_indexed_image(self):
        file_name = self.list_indexed_images_widget.currentFileName()
        explore(file_name, select=False)

    def view_details_indexed_image(self):
        file_name = self.list_indexed_images_widget.currentFileName()
        data = self.image_by_hashes[file_name]
        ImageHashDetailsDialog(file_name, data, parent=self).show()

    def select_similar_image(self):
        file_name = self.list_images_widget_similar.currentFileName()
        explore(file_name)

    def open_similar_image_directory(self):
        file_name = self.list_images_widget_similar.currentFileName()
        explore(Path(file_name).parent, select=False)

    def run_similar_image(self):
        file_name = self.list_images_widget_similar.currentFileName()
        explore(file_name, select=False)

    def view_details_similar_image(self):
        file_name = self.list_images_widget_similar.currentFileName()
        data = self.image_by_hashes[file_name]
        ImageHashDetailsDialog(file_name, data, parent=self).show()

    def read_settings(self):
        ini = QSettings(SETTINGS_FILE_NAME, QSettings.IniFormat)

        state = ini.value("MainWindow_State")
        if state:
            self.restoreState(state)

        geometry = ini.value("MainWindow_Geometry")
        if geometry:
            self.restoreGeometry(geometry)

        self.indexing_settings.read_settings(ini)
        self.search_for_similar_settings.read_settings(ini)

    def write_settings(self):
        ini = QSettings(SETTINGS_FILE_NAME, QSettings.IniFormat)
        ini.setValue("MainWindow_State", self.saveState())
        ini.setValue("MainWindow_Geometry", self.saveGeometry())

        self.indexing_settings.write_settings(ini)
        self.search_for_similar_settings.write_settings(ini)

    def closeEvent(self, event):
        self.write_settings()

        QApplication.closeAllWindows()


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.show()
    mw.resize(800, 600)

    mw.read_settings()

    mw.fill_images_db()

    app.exec()
