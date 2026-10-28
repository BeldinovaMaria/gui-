import sys
import os
import PyQt5

# --- 1. ВАЖНО: Указываем пути к плагинам и QML-модулям ДО импорта компонентов Qt ---
pyqt_dir = os.path.dirname(PyQt5.__file__)

# Путь к папке QML-модулей (QtQuick, QtQuick.Window и др.)
qml_import_path = os.path.join(pyqt_dir, "Qt5", "qml")
if not os.path.exists(qml_import_path):
    qml_import_path = os.path.join(pyqt_dir, "Qt", "qml")

# Путь к плагинам платформы
plugins_path = os.path.join(pyqt_dir, "Qt5", "plugins")
if not os.path.exists(plugins_path):
    plugins_path = os.path.join(pyqt_dir, "Qt", "plugins")

# Добавляем путь в переменные окружения ОС
os.environ["QML2_IMPORT_PATH"] = qml_import_path
os.environ["QT_PLUGIN_PATH"] = plugins_path