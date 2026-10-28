import os
from datetime import datetime
from PyQt5.QtCore import (
    QObject, QTimer, QMetaObject, Q_ARG, Q_RETURN_ARG,
    QVariant, pyqtSignal, pyqtSlot
)
from PyQt5.QtQml import QQmlApplicationEngine


# файл автосохранения лежит рядом с модулем, а не в текущей рабочей папке
SAVE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saved_canvas.png")


class Interface(QObject):

    # сигнал для QML: путь к файлу и время сохранения
    saved = pyqtSignal(str, str, arguments=["path", "time"])

    def __init__(self, engine=None, save_path=SAVE_PATH, interval_ms=5000):

        super().__init__()
        self.engine = engine if engine else QQmlApplicationEngine()
        self.save_path = save_path

        # флаг "есть несохраненные изменения" — выставляется из QML
        self.is_dirty = False

        # создаем таймер для автосохранения
        self.timer = QTimer(self)
        self.timer.setInterval(interval_ms)
        self.timer.timeout.connect(self.autosave)
        self.timer.start()

    @pyqtSlot()
    def markDirty(self):
        """Слот, вызываемый из QML после каждого изменения рисунка"""
        self.is_dirty = True

    def find_canvas(self):
        """Ищет объект canvas в загруженном QML"""
        root_objects = self.engine.rootObjects()
        if not root_objects:
            print("Ошибка: Не удалось получить корневой объект QML!")
            return None

        canvas = root_objects[0].findChild(QObject, "canvas")
        if canvas is None:
            print("Ошибка: Не удалось найти объект canvas в QML!")
        return canvas

    def save_canvas(self) -> bool:
        """Сохраняет canvas в файл и сообщает в QML о результате"""
        canvas = self.find_canvas()
        if canvas is None:
            return False

        # saveCanvas возвращает результат canvas.save(), поэтому ждем ответ
        result = QMetaObject.invokeMethod(
            canvas,
            "saveCanvas",
            Q_RETURN_ARG(QVariant),
            Q_ARG(QVariant, self.save_path)
        )

        if not result:
            print(f"[Backend] Ошибка: не удалось сохранить {self.save_path}")
            return False

        self.is_dirty = False
        time_str = datetime.now().strftime("%H:%M:%S")
        self.saved.emit(self.save_path, time_str)
        print(f"[Backend] {time_str} автосохранение выполнено: {self.save_path}")
        return True

    @pyqtSlot()
    def autosave(self):
        """Слот, вызываемый по таймеру: сохраняет только измененный рисунок"""
        if not self.is_dirty:
            return
        self.save_canvas()

    @pyqtSlot()
    def on_about_to_quit(self):
        """Последнее сохранение и очистка окружения перед выходом"""
        self.timer.stop()
        if self.is_dirty:
            self.save_canvas()
        self.cleanup_environment()

    def cleanup_environment(self):
        """Удаляет переменные окружения, выставленные в lab4_v2/__init__.py"""
        os.environ.pop("QML2_IMPORT_PATH", None)
        os.environ.pop("QT_PLUGIN_PATH", None)
        print("[System] Переменные окружения успешно очищены!")
