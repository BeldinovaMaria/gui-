from PyQt5.QtWidgets import QApplication
import sys

from lab1.image_switcher import ImageSwitcherApp


class LabPipeline():
    def __init__(self):
        pass

    
    def run_first_lab(self):
        app = QApplication(sys.argv)
        ex = ImageSwitcherApp()
        ex.show()
        sys.exit(app.exec_())