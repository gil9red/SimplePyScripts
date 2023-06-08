#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://stackoverflow.com/a/8551810/5909792


from PyQt5.Qt import QApplication, QSvgRenderer, QImage, Qt, QPainter


# A QApplication instance is necessary if fonts are used in the SVG
app = QApplication([])

# Load your SVG
renderer = QSvgRenderer("input.svg")

for width, height in [(32, 32), (64, 64), (512, 512), (4096, 4096)]:
    # Prepare a QImage with desired characteritisc
    image = QImage(width, height, QImage.Format_ARGB32)

    # Partly transparent red-ish background
    image.fill(Qt.transparent)

    # Get QPainter that paints to the image
    painter = QPainter(image)
    renderer.render(painter)

    # Save, image format based on file extension
    image.save("output_{}x{}.png".format(width, height))

    # FIX error: "Process finished with exit code -1073741819 (0xC0000005)"
    painter.end()
