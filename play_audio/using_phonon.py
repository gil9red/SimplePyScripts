#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        from PySide.QtCore import QCoreApplication
        from PySide.phonon import Phonon

        app = QCoreApplication(sys.argv)

        audio = Phonon.MediaObject()
        audio.setCurrentSource(Phonon.MediaSource(''))
        output = Phonon.AudioOutput(Phonon.MusicCategory)
        Phonon.createPath(audio, output)

        file_name = sys.argv[1]
        audio.setCurrentSource(Phonon.MediaSource(file_name))
        audio.play()

        audio.finished.connect(app.quit)

        quit(app.exec_())
    else:
        import os
        file_name = os.path.basename(sys.argv[0])
        print('usage: {} [-h] audio_file_name'.format(file_name))
