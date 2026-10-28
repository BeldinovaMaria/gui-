from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QTableView, QFileDialog, QAction, QComboBox,
    QPushButton, QLabel, QMessageBox
)
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from PyQt5.QtGui import QKeySequence

from lab3_v2.db_helper import DbHelper
from lab3_v2.query_dialog import QueryDialog


# имя соединения, чтобы не пересекаться с соединением по умолчанию
CONNECTION_NAME = "lab3_v2_connection"

# индексы вкладок
TAB_MASTER, TAB_NAMES, TAB_TABLE, TAB_STRUCTURE, TAB_COUNTS = range(5)


def quote_name(name: str) -> str:
    """Экранирует имя таблицы для подстановки в SQL-запрос"""
    return '"' + name.replace('"', '""') + '"'


class DbWindow(QMainWindow):
    def __init__(self):

        super().__init__()

        self.test_db_path = DbHelper.create_test_db()

        self.setWindowTitle("Лабораторная работа № 3 (v2)")
        self.setGeometry(100, 100, 900, 600)

        self.db = None

        # у каждой вкладки своя модель на всё время работы окна
        self.models = [QSqlQueryModel(self) for _ in range(5)]

        self.init_ui()

    @property
    def is_connected(self) -> bool:
        return self.db is not None and self.db.isOpen()

    def init_ui(self):
        # Меню приложения
        menubar = self.menuBar()
        connection_menu = menubar.addMenu("Соединение")

        act_connect = QAction("Set connection", self)
        act_connect.setShortcut(QKeySequence.Open)
        act_connect.triggered.connect(self.set_connection)
        connection_menu.addAction(act_connect)

        act_close = QAction("Close connection", self)
        act_close.setShortcut(QKeySequence("Ctrl+W"))
        act_close.triggered.connect(self.close_connection)
        connection_menu.addAction(act_close)

        query_menu = menubar.addMenu("Запрос")

        self.act_query = QAction("SQL-запрос...", self)
        self.act_query.setShortcut(QKeySequence("Ctrl+E"))
        self.act_query.triggered.connect(self.open_query_dialog)
        query_menu.addAction(self.act_query)

        # Центральный виджет и компоновка
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Панель управления (кнопки и QComboBox)
        control_layout = QHBoxLayout()

        self.btn_bt1 = QPushButton("bt1 (Имена объектов)")
        self.btn_bt1.clicked.connect(self.on_bt1_clicked)
        control_layout.addWidget(self.btn_bt1)

        control_layout.addWidget(QLabel("Таблица:"))
        self.combo_tables = QComboBox()
        self.combo_tables.setMinimumWidth(150)
        self.combo_tables.currentTextChanged.connect(self.on_combo_changed)
        control_layout.addWidget(self.combo_tables)

        self.btn_bt2 = QPushButton("bt2 (Структура таблицы)")
        self.btn_bt2.clicked.connect(self.on_bt2_clicked)
        control_layout.addWidget(self.btn_bt2)

        self.btn_bt3 = QPushButton("bt3 (Количество строк)")
        self.btn_bt3.clicked.connect(self.on_bt3_clicked)
        control_layout.addWidget(self.btn_bt3)

        control_layout.addStretch()
        main_layout.addLayout(control_layout)

        # Вкладки (QTabWidget), по умолчанию пустые
        self.tabs = QTabWidget()
        self.tab_views = []

        for i, model in enumerate(self.models, start=1):
            table_view = QTableView()
            table_view.setModel(model)
            table_view.setAlternatingRowColors(True)
            self.tabs.addTab(table_view, f"Tab{i}")
            self.tab_views.append(table_view)

        main_layout.addWidget(self.tabs)

        self.statusBar().showMessage("Нет соединения с БД")

        # Блокируем элементы управления до подключения
        self.set_controls_enabled(False)

    def set_controls_enabled(self, state: bool):
        """Включение/выключение элементов управления"""
        for widget in (self.btn_bt1, self.btn_bt2, self.btn_bt3, self.combo_tables):
            widget.setEnabled(state)
        self.act_query.setEnabled(state)

    def show_query(self, query_str: str, tab_index: int, switch_tab: bool = True) -> bool:
        """Выполняет SQL-запрос и выводит результат в указанную вкладку"""
        if not self.is_connected:
            return False

        model = self.models[tab_index]
        model.setQuery(query_str, self.db)

        if model.lastError().isValid():
            QMessageBox.warning(self, "Ошибка БД", f"Ошибка выполнения запроса:\n{model.lastError().text()}")
            DbHelper.release_model(model)
            return False

        self.tab_views[tab_index].resizeColumnsToContents()
        if switch_tab:
            self.tabs.setCurrentIndex(tab_index)

        self.statusBar().showMessage(
            f"{self.db.databaseName()} | Tab{tab_index + 1}: строк — {model.rowCount()}"
        )
        return True

    def set_connection(self):
        """Открытие диалогового окна и подключение к SQLite БД"""
        db_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл базы данных SQLite", self.test_db_path,
            "SQLite Databases (*.db *.sqlite *.sqlite3);;All Files (*)"
        )

        if not db_path:
            return

        # Если было старое подключение — тихо закрываем его
        self.disconnect_db()

        if not self.connect_db(db_path):
            return

        QMessageBox.information(self, "Успех", f"Соединение с БД успешно установлено!\n{db_path}")

    def connect_db(self, db_path: str) -> bool:
        """Открывает соединение и заполняет интерфейс начальными данными"""
        db = QSqlDatabase.addDatabase("QSQLITE", CONNECTION_NAME)
        db.setDatabaseName(db_path)

        if not db.open():
            error_text = db.lastError().text()
            del db
            QSqlDatabase.removeDatabase(CONNECTION_NAME)
            QMessageBox.critical(self, "Ошибка", f"Не удалось подключиться к базе данных!\n{error_text}")
            return False

        self.db = db

        # SQLite откроет любой файл, поэтому проверяем, что это действительно БД
        if not self.show_query("SELECT * FROM sqlite_master", TAB_MASTER):
            self.disconnect_db()
            return False

        self.set_controls_enabled(True)
        self.load_table_names()
        self.tabs.setCurrentIndex(TAB_MASTER)
        return True

    def load_table_names(self):
        """Загрузка списка таблиц и представлений в QComboBox"""
        self.combo_tables.blockSignals(True)
        self.combo_tables.clear()

        query = QSqlQuery(self.db)
        query.exec_(
            "SELECT name FROM sqlite_master "
            "WHERE type IN ('table', 'view') AND name NOT LIKE 'sqlite_%' "
            "ORDER BY type, name"
        )
        while query.next():
            self.combo_tables.addItem(query.value(0))

        self.combo_tables.blockSignals(False)

        # Если таблицы есть, сразу загружаем первую в Tab3
        if self.combo_tables.count() > 0:
            self.on_combo_changed(self.combo_tables.currentText(), switch_tab=False)

    def disconnect_db(self):
        """Очищает модели и закрывает соединение с БД"""
        # Модели держат запросы к соединению — освобождаем их до закрытия
        for model in self.models:
            DbHelper.release_model(model)

        self.combo_tables.blockSignals(True)
        self.combo_tables.clear()
        self.combo_tables.blockSignals(False)

        if self.db is not None:
            self.db.close()
            self.db = None
            QSqlDatabase.removeDatabase(CONNECTION_NAME)

        self.set_controls_enabled(False)
        self.statusBar().showMessage("Нет соединения с БД")

    def close_connection(self):
        """Обработчик пункта меню Close connection"""
        if not self.is_connected:
            QMessageBox.information(self, "Соединение", "Соединение с БД не установлено.")
            return

        self.disconnect_db()
        QMessageBox.information(self, "Соединение", "Соединение с БД закрыто, интерфейс очищен.")

    def open_query_dialog(self):
        """Открывает модальное окно для произвольного запроса"""
        if not self.is_connected:
            return

        dialog = QueryDialog(self.db, self)
        dialog.exec_()
        dialog.deleteLater()

    def closeEvent(self, event):
        self.disconnect_db()
        super().closeEvent(event)

    # --- Обработчики сигналов ---

    def on_bt1_clicked(self):
        """bt1: выборочный запрос — имена всех объектов БД (Tab2)"""
        self.show_query("SELECT name FROM sqlite_master ORDER BY name", TAB_NAMES)

    def on_combo_changed(self, table_name: str, switch_tab: bool = True):
        """Выбор таблицы в QComboBox: все записи таблицы (Tab3)"""
        if table_name:
            self.show_query(f"SELECT * FROM {quote_name(table_name)}", TAB_TABLE, switch_tab)

    def on_bt2_clicked(self):
        """bt2: структура (колонки) выбранной таблицы (Tab4)"""
        table_name = self.combo_tables.currentText()
        if table_name:
            self.show_query(f"PRAGMA table_info({quote_name(table_name)})", TAB_STRUCTURE)

    def on_bt3_clicked(self):
        """bt3: количество записей в каждой таблице (Tab5)"""
        tables = [self.combo_tables.itemText(i) for i in range(self.combo_tables.count())]
        if not tables:
            return

        # запрос собирается динамически из списка таблиц
        query_str = " UNION ALL ".join(
            f"SELECT '{name.replace(chr(39), chr(39) * 2)}' AS table_name, "
            f"COUNT(*) AS rows_count FROM {quote_name(name)}"
            for name in tables
        )
        self.show_query(query_str, TAB_COUNTS)
