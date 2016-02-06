#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os.path
import sys

from PySide.QtGui import *
from PySide.QtCore import *

import dirs_sizes


logger = dirs_sizes.get_logger('dirs_sizes_gui')


def dir_size_bytes(dir_path, root_item, files=0, dirs=0, level=0, do_indent=True, size_less=dirs_sizes.get_bytes('1 GB')):
    it = QDirIterator(dir_path, '*.*', QDir.AllEntries | QDir.NoDotAndDotDot | QDir.Hidden | QDir.System)

    sizes = 0

    row = [QStandardItem(os.path.normpath(dir_path)), QStandardItem('-')]

    while it.hasNext():
        file_name = it.next()
        file = QFileInfo(file_name)

        if file.isDir():
            # row = [QStandardItem(os.path.normpath(file_name)), QStandardItem('-')]
            # root_item.appendRow(row)

            dirs += 1
            size, files, dirs = dir_size_bytes(file_name, row[0], files, dirs, level + 1, do_indent, size_less)

            # row[1].setText(dirs_sizes.pretty_file_size(size)[1])
        else:
            files += 1
            size = file.size()

        sizes += size

    if sizes >= size_less:
        root_item.appendRow(row)
        row[1].setText(dirs_sizes.pretty_file_size(sizes)[1])

        # row[1].setText(dirs_sizes.pretty_file_size(sizes)[1])
        # root_item.appendRow(row)

        logger.debug(
            ((' ' * 4 * level) if do_indent else '')
            + os.path.normpath(dir_path) + ' ' + '{1} ({0} bytes)'.format(*dirs_sizes.pretty_file_size(sizes))
        )

    return sizes, files, dirs


if __name__ == '__main__':
    app = QApplication(sys.argv)

    model = QStandardItemModel()
    header_labels = ['Имя', 'Размер']
    model.setColumnCount(len(header_labels))
    model.setHorizontalHeaderLabels(header_labels)

    sizes, files, dirs = dir_size_bytes(r'C:\\', model.invisibleRootItem())
    # row[1].setText(dirs_sizes.pretty_file_size(sizes)[1])

    # for drive in QDir.drives():
    #     drive_name = drive.path()
    #
    #     if 'C:' in drive_name:
    #         row = [QStandardItem(drive.path()), QStandardItem(drive.size())]
    #         model.appendRow(row)
    #
    #         sizes, files, dirs = dir_size_bytes(drive_name, row[0])
    #         row[1].setText(dirs_sizes.pretty_file_size(sizes)[1])

    tree = QTreeView()
    tree.setModel(model)
    tree.setAnimated(False)
    tree.setIndentation(20)
    # tree.setSortingEnabled(True)

    tree.setWindowTitle("Dirs Sizes")
    tree.resize(640, 480)
    tree.show()

    sys.exit(app.exec_())
