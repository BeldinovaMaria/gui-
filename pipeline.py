from PyQt5.QtWidgets import QApplication
import sys

from lab1.image_switcher import ImageSwitcherApp
from lab2.value_converter import CurrencyConverterApp


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