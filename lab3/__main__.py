import sys
from PyQt5.QtWidgets import QApplication

from lab3_v2.db_window import DbWindow


# запуск из корня репозитория: python -m lab3_v2
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DbWindow()
    window.show()
    sys.exit(app.exec_())
