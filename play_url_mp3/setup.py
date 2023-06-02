# -*- coding: utf-8 -*-

# A very simple setup script to create a single executable
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python

from cx_Freeze import setup, Executable

executables = [Executable("play_url_mp3.py")]

setup(
    name="play_url_mp3",
    version="0.1",
    description="play_url_mp3.py",
    executables=executables,
)
