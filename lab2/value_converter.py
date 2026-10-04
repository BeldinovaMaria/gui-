from PyQt5.QtWidgets import (
    QFormLayout,
    QLabel,
    QLineEdit,
    QWidget,
)


class CurrencyConverterApp(QWidget):

  def __init__(self):
    super().__init__()
    self.initUI()
    # Флаг для предотвращения бесконечной рекурсии сигналов
    self.updating = False

  def initUI(self):
    self.setWindowTitle("Лабораторная работа: Связанные данные (Валюты)")
    self.resize(350, 200)

    layout = QFormLayout()

    # Создаем поля ввода
    self.input_rub = QLineEdit("100.0")
    self.input_usd = QLineEdit("1.0")
    self.input_eur = QLineEdit("0.92")

    layout.addRow(QLabel("<b>Рубли (RUB):</b>"), self.input_rub)
    layout.addRow(QLabel("<b>Доллары (USD):</b>"), self.input_usd)
    layout.addRow(QLabel("<b>Евро (EUR):</b>"), self.input_eur)

    self.setLayout(layout)

    # Привязываем сигналы изменения текста к соответствующим слотам
    self.input_rub.textChanged.connect(
        lambda: self.convert("rub", self.input_rub.text())
    )
    self.input_usd.textChanged.connect(
        lambda: self.convert("usd", self.input_usd.text())
    )
    self.input_eur.textChanged.connect(
        lambda: self.convert("eur", self.input_eur.text())
    )

  def convert(self, source, text):
    if self.updating:
      return

    self.updating = True

    try:
      # Пустое поле сбрасывает остальные
      if not text:
        if source != "rub":
          self.input_rub.clear()
        if source != "usd":
          self.input_usd.clear()
        if source != "eur":
          self.input_eur.clear()
        self.updating = False
        return

      val = float(text)

      # Условные фиксированные курсы для примера
      # 1 USD = 100 RUB, 1 EUR = 109 RUB
      if source == "rub":
        usd = val / 100.0
        eur = val / 109.0
        self.input_usd.setText(f"{usd:.2f}")
        self.input_eur.setText(f"{eur:.2f}")

      elif source == "usd":
        rub = val * 100.0
        eur = (val * 100.0) / 109.0
        self.input_rub.setText(f"{rub:.2f}")
        self.input_eur.setText(f"{eur:.2f}")

      elif source == "eur":
        rub = val * 109.0
        usd = (val * 109.0) / 100.0
        self.input_rub.setText(f"{rub:.2f}")
        self.input_usd.setText(f"{usd:.2f}")

    except ValueError:
      # Игнорируем некорректный ввод (например, буквы)
      pass

    self.updating = False