pyside-uic -o mainwindow_ui.py mainwindow.ui
:: pyside-uic -o settings_ui.py settings.ui
:: pyside-uic -o pluginmanager_ui.py pluginmanager.ui

:: pyside-rcc -o resource_rc.py resource.qrc
:: Problem with qRegisterResourceData:
:: https://chr0n0m3t3r.wordpress.com/2014/04/03/build-pyside-with-python-3-4/