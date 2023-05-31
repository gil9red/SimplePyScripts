#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: http://itnotesblog.ru/note.php?id=272#sthash.e5tCuHk0.dpbs


import sys
import traceback

from PyQt5 import Qt
from PyQt5 import uic

# pip install opencv-python
import cv2

import numpy as np


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    print(text)
    Qt.QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


CONFIG_FILE_NAME = "config.ini"
WINDOW_TITLE = "Color Detection Tool"
GRAY_COLOR_TABLE = [Qt.qRgb(i, i, i) for i in range(256)]


def numpy_array_to_QImage(numpy_array):
    if numpy_array.dtype != np.uint8:
        return

    height, width = numpy_array.shape[:2]

    if len(numpy_array.shape) == 2:
        img = Qt.QImage(
            numpy_array.data,
            width,
            height,
            numpy_array.strides[0],
            Qt.QImage.Format_Indexed8,
        )
        img.setColorTable(GRAY_COLOR_TABLE)
        return img

    elif len(numpy_array.shape) == 3:
        if numpy_array.shape[2] == 3:
            img = Qt.QImage(
                numpy_array.data,
                width,
                height,
                numpy_array.strides[0],
                Qt.QImage.Format_RGB888,
            )
            return img

        elif numpy_array.shape[2] == 4:
            img = Qt.QImage(
                numpy_array.data,
                width,
                height,
                numpy_array.strides[0],
                Qt.QImage.Format_ARGB32,
            )
            return img


class MainWindow(Qt.QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi("mainwidget.ui", self)

        self.setWindowTitle(WINDOW_TITLE)

        self.cbPenStyle.addItem("Solid", Qt.Qt.SolidLine)
        self.cbPenStyle.addItem("Dash", Qt.Qt.DashLine)
        self.cbPenStyle.addItem("Dot", Qt.Qt.DotLine)
        self.cbPenStyle.addItem("Dash Dot", Qt.Qt.DashDotLine)
        self.cbPenStyle.addItem("Dash Dot Dot", Qt.Qt.DashDotDotLine)

        self.pen_color = Qt.QColor(Qt.Qt.green)
        self.last_load_path = "."

        self.image_source = None
        self.result_img = None

        self.load_settings()

        for w in self.findChildren(Qt.QSlider):
            w.sliderMoved.connect(self.refresh_HSV)

            name = w.objectName()
            sp = self.findChild(Qt.QSpinBox, "sp" + name[2:])
            if not sp:
                continue

            sp.setMinimum(w.minimum())
            sp.setMaximum(w.maximum())
            sp.setValue(w.value())
            sp.valueChanged.connect(self.refresh_HSV)

        self.rbOriginal.clicked.connect(self.refresh_HSV)
        self.rbThresholded.clicked.connect(self.refresh_HSV)
        self.rbCanny.clicked.connect(self.refresh_HSV)
        self.rbResult.clicked.connect(self.refresh_HSV)
        self.cbResultHSV.clicked.connect(self.refresh_HSV)
        self.chOnlyExternal.clicked.connect(self.refresh_HSV)

        self.cbPenStyle.currentIndexChanged.connect(self.refresh_HSV)
        self.sbPenWidth.valueChanged.connect(self.refresh_HSV)

        self.bnLoad.clicked.connect(self.on_load)
        self.pbPenColor.clicked.connect(self._choose_color)

        self._update_pen_color()
        self.refresh_HSV()

    def on_load(self):
        image_filters = "Images (*.jpg *.jpeg *.png *.bmp)"
        file_name = Qt.QFileDialog.getOpenFileName(
            self, "Load image", self.last_load_path, image_filters
        )[0]
        if not file_name:
            return

        self.last_load_path = Qt.QFileInfo(file_name).absolutePath()

        # Load image as bytes
        with open(file_name, "rb") as f:
            img_data = f.read()

        nparr = np.frombuffer(img_data, np.uint8)
        self.image_source = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)

        height, width, channels = self.image_source.shape
        self.setWindowTitle(
            f"{WINDOW_TITLE}. {width}x{height} ({channels} channels). {file_name}"
        )

        # Трансформация BGR->RGB если 3 канала. У картинок с прозрачностью каналов 4 и для них почему
        if channels == 3:
            code = cv2.COLOR_BGR2RGB

        elif channels == 4:
            code = cv2.COLOR_BGRA2RGB

        else:
            raise Exception(f"Unexpected number of channels: {channels}")

        self.image_source = cv2.cvtColor(self.image_source, code)

        self.refresh_HSV()

    def show_result(self):
        if not self.result_img:
            return

        size = self.lbView.size()
        pixmap = Qt.QPixmap.fromImage(self.result_img).scaled(
            size, Qt.Qt.KeepAspectRatio, Qt.Qt.SmoothTransformation
        )
        self.lbView.setPixmap(pixmap)

    def _update_pen_color(self):
        palette = self.pbPenColor.palette()
        palette.setColor(Qt.QPalette.Button, self.pen_color)
        self.pbPenColor.setPalette(palette)

    def _choose_color(self):
        color = Qt.QColorDialog.getColor(self.pen_color)
        if not color.isValid():
            return

        self.pen_color = color

        self._update_pen_color()
        self.refresh_HSV()

    def _draw_contours(self, result_img, contours):
        line_size = self.sbPenWidth.value()
        line_type = self.cbPenStyle.currentData()
        line_color = self.pen_color

        p = Qt.QPainter(result_img)
        p.setPen(Qt.QPen(line_color, line_size, line_type))

        for c in contours:
            x, y, width, height = cv2.boundingRect(c)
            p.drawRect(x, y, width, height)

        p.end()

    def refresh_HSV(self):
        hue_from = self.slHueFrom.value()
        hue_to = max(hue_from, self.slHueTo.value())

        saturation_from = self.slSaturationFrom.value()
        saturation_to = max(saturation_from, self.slSaturationTo.value())

        value_from = self.slValueFrom.value()
        value_to = max(value_from, self.slValueTo.value())

        hsv_min = hue_from, saturation_from, value_from
        hsv_max = hue_to, saturation_to, value_to

        color_hsv_min = Qt.QColor.fromHsv(*hsv_min)
        color_hsv_max = Qt.QColor.fromHsv(*hsv_max)

        self.label_hsv_from_text.setText(", ".join(map(str, hsv_min)))
        self.label_hsv_to_text.setText(", ".join(map(str, hsv_max)))

        pixmap = Qt.QPixmap(1, 1)
        pixmap.fill(color_hsv_min)
        self.lbHsvMin.setPixmap(pixmap)

        pixmap = Qt.QPixmap(1, 1)
        pixmap.fill(color_hsv_max)
        self.lbHsvMax.setPixmap(pixmap)

        if self.image_source is None:
            return

        if self.rbOriginal.isChecked():
            self.result_img = numpy_array_to_QImage(self.image_source)

        else:
            thresholded_image = cv2.cvtColor(self.image_source, cv2.COLOR_RGB2HSV)

            # Отфильтровываем только то, что нужно, по диапазону цветов
            thresholded_image = cv2.inRange(
                thresholded_image,
                np.array(hsv_min, np.uint8),
                np.array(hsv_max, np.uint8),
            )

            # Убираем шум
            thresholded_image = cv2.erode(
                thresholded_image, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            )
            thresholded_image = cv2.dilate(
                thresholded_image, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            )

            # Замыкаем оставшиеся крупные объекты
            thresholded_image = cv2.dilate(
                thresholded_image, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            )
            thresholded_image = cv2.erode(
                thresholded_image, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            )

            if self.rbCanny.isChecked():
                # Визуально выделяем границы
                thresholded_image = cv2.Canny(thresholded_image, 100, 50, 5)

            if self.rbResult.isChecked():
                mode = (
                    cv2.RETR_EXTERNAL
                    if self.chOnlyExternal.isChecked()
                    else cv2.RETR_TREE
                )

                # Находим контуры
                contours, _ = cv2.findContours(
                    thresholded_image, mode, cv2.CHAIN_APPROX_SIMPLE
                )

                result_img = self.image_source.copy()

                # Конвертирование цвета в HSV
                if self.cbResultHSV.isChecked():
                    result_img = cv2.cvtColor(result_img, cv2.COLOR_RGB2HSV)

                self.result_img = numpy_array_to_QImage(result_img)
                self._draw_contours(self.result_img, contours)

            else:
                self.result_img = numpy_array_to_QImage(thresholded_image)

        self.show_result()

    def save_settings(self):
        settings = Qt.QSettings(CONFIG_FILE_NAME, Qt.QSettings.IniFormat)

        settings.setValue(self.objectName(), self.saveGeometry())

        # TODO: рефакторинг циклов

        for w in self.findChildren(Qt.QComboBox):
            name = w.objectName()
            settings.setValue(name, w.currentIndex())

        for w in self.findChildren(Qt.QRadioButton):
            name = w.objectName()
            settings.setValue(name, int(w.isChecked()))

        for w in self.findChildren(Qt.QSlider):
            name = w.objectName()
            settings.setValue(name, w.value())

        for w in self.findChildren(Qt.QDoubleSpinBox):
            name = w.objectName()
            settings.setValue(name, w.value())

        for w in self.findChildren(Qt.QSpinBox):
            name = w.objectName()
            settings.setValue(name, w.value())

        for w in self.findChildren(Qt.QCheckBox):
            name = w.objectName()
            settings.setValue(name, int(w.isChecked()))

        settings.setValue("PenColor", self.pen_color.name())

        settings.setValue("lastLoadPath", self.last_load_path)

    def load_settings(self):
        settings = Qt.QSettings(CONFIG_FILE_NAME, Qt.QSettings.IniFormat)

        geometry = settings.value(self.objectName())
        if geometry:
            self.restoreGeometry(geometry)

        self.last_load_path = settings.value("lastLoadPath", ".")

        self.pen_color = Qt.QColor(settings.value("PenColor", Qt.Qt.green))

        # TODO: рефакторинг циклов

        for w in self.findChildren(Qt.QComboBox):
            name = w.objectName()
            value = int(settings.value(name, w.currentIndex()))
            w.setCurrentIndex(value)

        for w in self.findChildren(Qt.QRadioButton):
            name = w.objectName()
            value = bool(int(settings.value(name, w.isChecked())))
            w.setChecked(value)

        for w in self.findChildren(Qt.QSpinBox):
            name = w.objectName()
            value = int(settings.value(name, w.value()))
            w.setValue(value)

        for w in self.findChildren(Qt.QDoubleSpinBox):
            name = w.objectName()
            value = float(settings.value(name, w.value()))
            w.setValue(value)

        for w in self.findChildren(Qt.QCheckBox):
            name = w.objectName()
            value = bool(int(settings.value(name, w.isChecked())))
            w.setChecked(value)

        for w in self.findChildren(Qt.QSlider):
            name = w.objectName()
            value = int(settings.value(name, w.value()))
            w.setValue(value)

            sp = self.findChild(Qt.QSpinBox, "sp" + name[2:])
            if sp:
                sp.setMinimum(w.minimum())
                sp.setMaximum(w.maximum())
                sp.setValue(w.value())

    def resizeEvent(self, e):
        super().resizeEvent(e)

        self.show_result()

    def closeEvent(self, e):
        self.save_settings()

        super().closeEvent(e)


if __name__ == "__main__":
    app = Qt.QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
