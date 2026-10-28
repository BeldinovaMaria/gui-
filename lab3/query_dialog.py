from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPlainTextEdit,
    QPushButton, QLabel, QTableView, QDialogButtonBox
)
from PyQt5.QtSql import QSqlQueryModel

from lab3_v2.db_helper import DbHelper


class QueryDialog(QDialog):
    """Модальное окно для выполнения произвольного SQL-запроса (бонусное задание)"""

    def __init__(self, db, parent=None):

        super().__init__(parent)

        self.db = db

        self.setWindowTitle("SQL-запрос")
        self.setModal(True)
        self.resize(700, 450)

        self.model = QSqlQueryModel(self)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Введите SQL-запрос:"))

        self.edit_query = QPlainTextEdit()
        self.edit_query.setPlainText("SELECT * FROM sqlite_master")
        self.edit_query.setFixedHeight(90)
        layout.addWidget(self.edit_query)

        run_layout = QHBoxLayout()
        self.lbl_status = QLabel()
        run_layout.addWidget(self.lbl_status, 1)

        btn_run = QPushButton("Выполнить")
        btn_run.setDefault(True)
        btn_run.clicked.connect(self.run_query)
        run_layout.addWidget(btn_run)
        layout.addLayout(run_layout)

        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        layout.addWidget(self.table_view)

        buttons = QDialogButtonBox(QDialogButtonBox.Close)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def run_query(self):
        """Выполняет введенный запрос и показывает результат в таблице окна"""
        query_str = self.edit_query.toPlainText().strip()
        if not query_str or self.db is None:
            return

        self.model.setQuery(query_str, self.db)

        if self.model.lastError().isValid():
            self.lbl_status.setText(f"Ошибка: {self.model.lastError().text()}")
            return

        self.table_view.resizeColumnsToContents()
        self.lbl_status.setText(f"Строк в результате: {self.model.rowCount()}")

    def done(self, result):
        # освобождаем запрос и ссылку на БД, чтобы соединение можно было закрыть
        DbHelper.release_model(self.model)
        self.db = None
        super().done(result)
