import sys
import os
import PyQt5
from PyQt5.QtCore import QCoreApplication

## фикс ошибки Driver not found

# находим папку с плагинами PyQt5
pyqt_dir = os.path.dirname(PyQt5.__file__)
plugins_dir = os.path.join(pyqt_dir, "Qt5", "plugins")

# если структуры Qt5 нет, проверяем прямую папку Qt/plugins
if not os.path.exists(plugins_dir):
    plugins_dir = os.path.join(pyqt_dir, "Qt", "plugins")

# добавляем путь к библиотекам ДО создания QApplication
QCoreApplication.addLibraryPath(plugins_dir)