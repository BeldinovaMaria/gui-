from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QLabel, QPushButton,
                             QVBoxLayout, QWidget)


class ImageSwitcherApp(QWidget):

  def __init__(self):
    super().__init__()

    self.image_path = "lab1/autumn.jpg"
    self.initUI()

  def initUI(self):
    """Настройки основного окна"""

    self.setWindowTitle("Замена текста на картинку в PyQt5")
    self.resize(400, 400)

    layout = QVBoxLayout()

    self.label = QLabel("Нажмите кнопку, чтобы показать картинку", self)
    self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(self.label)

    self.button = QPushButton("Показать картинку", self)
    self.button.clicked.connect(self.change_to_image)   # Подключаем сигнал нажатия кнопки к нашему методу
    layout.addWidget(self.button)

    self.setLayout(layout)

  def change_to_image(self):
    pixmap = QPixmap(self.image_path)

    if not pixmap.isNull():
      # Масштабируем картинку под размер метки с сохранением пропорций
      scaled_pixmap = pixmap.scaled(
          300, 300, 
          Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
      )
     
      self.label.setPixmap(scaled_pixmap)
      self.button.setEnabled(False)
    else:
      self.label.setText(
          "Не удалось найти файл 'image.png'!\nПроверьте путь к файлу."
      )