from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QUrl
import sys

from lab1.image_switcher import ImageSwitcherApp
from lab2.value_converter import CurrencyConverterApp
from lab3.db_window import DbWindow
from lab4.interface import Interface


class LabPipeline():
    def __init__(self):
        pass

    
    def run_first_lab(self):
        app = QApplication(sys.argv)
        ex = ImageSwitcherApp()
        ex.show()
        sys.exit(app.exec_())


    def run_second_lab(self):
        app = QApplication(sys.argv)
        ex = CurrencyConverterApp()
        ex.show()
        sys.exit(app.exec_())


    def run_third_lab(self):
        app = QApplication(sys.argv)

        window = DbWindow()
        window.show()
        sys.exit(app.exec_())


    def run_four_lab(self):
        app = QApplication(sys.argv)

        engine = QQmlApplicationEngine()
        interface = Interface(engine)

        app.aboutToQuit.connect(interface.on_about_to_quit)

        # контекстное свойство нужно выставить до загрузки QML
        engine.rootContext().setContextProperty("_backend", interface)

        engine.load(QUrl.fromLocalFile(QML_PATH))

        if not engine.rootObjects():
            print("Ошибка: Не удалось загрузить QML файл!")
            sys.exit(-1)

        sys.exit(app.exec_())