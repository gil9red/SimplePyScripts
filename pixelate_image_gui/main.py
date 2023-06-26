#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
import sys
import traceback

from PIL import Image

from PyQt5 import Qt


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/1c1ad83de7c0f0bd02d9926fe141da4ba5b92720/pil_example/pixelate_image/main.py
def pixelate(image, pixel_size=9, draw_margin=True):
    margin_color = (0, 0, 0)

    image = image.resize(
        (image.size[0] // pixel_size, image.size[1] // pixel_size), Image.NEAREST
    )
    image = image.resize(
        (image.size[0] * pixel_size, image.size[1] * pixel_size), Image.NEAREST
    )
    pixel = image.load()

    # Draw black margin between pixels
    if draw_margin:
        for i in range(0, image.size[0], pixel_size):
            for j in range(0, image.size[1], pixel_size):
                for r in range(pixel_size):
                    pixel[i + r, j] = margin_color
                    pixel[i, j + r] = margin_color

    return image


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    print(text)
    Qt.QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


WINDOW_TITLE = "Pixelate"


class MainWindow(Qt.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(WINDOW_TITLE)

        self.last_load_path = "."
        self.file_name = None
        self.image_source = None
        self.image_result = None

        self.lb_image_view = Qt.QLabel()
        self.lb_image_view.setAlignment(Qt.Qt.AlignCenter)

        self.pb_load_image = Qt.QPushButton("Load")
        self.pb_load_image.clicked.connect(self.load)

        self.pb_save_as = Qt.QPushButton("Save as...")
        self.pb_save_as.clicked.connect(self.save_as)

        self.rb_original = Qt.QRadioButton("Original")
        self.rb_original.clicked.connect(self._do_pixelate)

        self.rb_result = Qt.QRadioButton("Result")
        self.rb_result.setChecked(True)
        self.rb_result.clicked.connect(self._do_pixelate)

        self.cb_draw_margin = Qt.QCheckBox("Draw margin")
        self.cb_draw_margin.setChecked(True)
        self.cb_draw_margin.clicked.connect(self._do_pixelate)

        self.sl_pixel_size = Qt.QSlider(Qt.Qt.Horizontal)
        self.sl_pixel_size.setRange(2, 200)
        self.sl_pixel_size.setValue(9)

        self.sb_pixel_size = Qt.QSpinBox()
        self.sb_pixel_size.setRange(
            self.sl_pixel_size.minimum(), self.sl_pixel_size.maximum()
        )
        self.sb_pixel_size.setValue(self.sl_pixel_size.value())

        self.sl_pixel_size.sliderMoved.connect(self.sb_pixel_size.setValue)
        self.sb_pixel_size.valueChanged.connect(self.sl_pixel_size.setValue)

        self.sl_pixel_size.sliderMoved.connect(self._do_pixelate)
        self.sb_pixel_size.valueChanged.connect(self._do_pixelate)

        line = Qt.QFrame()
        line.setFrameShape(Qt.QFrame.HLine)
        line.setFrameShadow(Qt.QFrame.Sunken)

        layout_button = Qt.QHBoxLayout()
        layout_button.addWidget(self.rb_original)
        layout_button.addWidget(self.rb_result)
        layout_button.addStretch()
        layout_button.addWidget(self.cb_draw_margin)

        layout_button_2 = Qt.QHBoxLayout()
        layout_button_2.addWidget(Qt.QLabel("Pixel size:"))
        layout_button_2.addWidget(self.sl_pixel_size)
        layout_button_2.addWidget(self.sb_pixel_size)

        main_layout = Qt.QVBoxLayout()
        main_layout.addWidget(self.lb_image_view)
        main_layout.addWidget(self.pb_load_image)
        main_layout.addWidget(line)
        main_layout.addLayout(layout_button)
        main_layout.addLayout(layout_button_2)
        main_layout.addWidget(self.pb_save_as)

        self.setLayout(main_layout)

        self._do_pixelate()

    def load(self):
        image_filters = "Images (*.jpg *.jpeg *.png *.bmp)"
        self.file_name = Qt.QFileDialog.getOpenFileName(
            self, "Load image", self.last_load_path, image_filters
        )[0]
        if not self.file_name:
            return

        self.last_load_path = Qt.QFileInfo(self.file_name).absolutePath()
        self.image_source = Image.open(self.file_name).convert("RGB")

        self._do_pixelate()

    def save_as(self):
        image_filters = "Images (*.jpg *.jpeg *.png *.bmp)"

        # C:\Images\img.png -> C:\Images\img_pixelate.png
        file_name = "_pixelate".join(os.path.splitext(self.file_name))

        file_name = Qt.QFileDialog.getSaveFileName(
            self, "Save as image", file_name, image_filters
        )[0]
        if not file_name:
            return

        self.image_result.save(file_name)

    def _do_pixelate(self):
        # Виджеты будут доступны только если стоит флаг на Result и картинка загружена
        ok = self.rb_result.isChecked() and self.image_source is not None
        self.pb_save_as.setEnabled(ok)
        self.cb_draw_margin.setEnabled(ok)
        self.sl_pixel_size.setEnabled(ok)
        self.sb_pixel_size.setEnabled(ok)

        # Делаем пиксеализацию
        if ok:
            pixel_size = self.sl_pixel_size.value()
            draw_margin = self.cb_draw_margin.isChecked()

            self.image_result = pixelate(self.image_source, pixel_size, draw_margin)

        self.show_result()

    def show_result(self):
        image_result = self.image_result if self.rb_result.isChecked() else self.image_source
        if not image_result:
            return

        image_result = image_result.toqpixmap()

        size = self.lb_image_view.size()
        pixmap = image_result.scaled(
            size, Qt.Qt.KeepAspectRatio, Qt.Qt.SmoothTransformation
        )
        self.lb_image_view.setPixmap(pixmap)

        height, width = self.image_source.size
        title = f"{WINDOW_TITLE}. {width}x{height} ({size.width()}x{size.height()}). {self.file_name}"
        self.setWindowTitle(title)

    def resizeEvent(self, e):
        super().resizeEvent(e)

        self.show_result()


if __name__ == "__main__":
    app = Qt.QApplication([])

    mw = MainWindow()
    mw.setMinimumSize(400, 400)
    mw.show()

    app.exec()
