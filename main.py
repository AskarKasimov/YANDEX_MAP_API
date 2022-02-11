import os
import requests
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QLabel, QLineEdit

URL = "http://static-maps.yandex.ru/1.x"

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.scale = 0

    def initUI(self):
        self.setGeometry(300, 300, 400, 400)
        self.setWindowTitle('Часть 1')

        self.btn = QPushButton('Сформировать карту', self)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(100, 100)
        self.btn.clicked.connect(self.setScale)

        self.label = QLabel(self)
        self.label.setText("Укажите координаты")
        self.label.move(20, 10)

        self.name_label = QLabel(self)
        self.name_label.setText("Укажите масштаб")
        self.name_label.move(20, 70)

        self.longitude = QLineEdit(self)
        self.longitude.move(170, 10)
        self.latitude = QLineEdit(self)
        self.latitude.move(170, 30)
        self.edit_scale = QLineEdit(self)
        self.edit_scale.move(170, 70)

        self.image = QLabel(self)
        self.image.move(5, 125)
        self.image.resize(390, 270)

    def setScale(self):
        self.scale = float(self.edit_scale.text())
        self.getImage()

    def getImage(self):
        params = {
            "ll": f"{self.longitude.text()},{self.latitude.text()}",
            "spn": f"{self.scale},{self.scale}",
            "l": "map",
            "size": "390,270"
        }
        print(params)
        response = requests.get(URL, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

        ## Изображение
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp and self.scale > 0.3:
            self.scale = round(self.scale - 0.3, 4)
        elif event.key() == Qt.Key_PageDown and self.scale < 40:
            self.scale = round(self.scale + 0.3, 4)
        self.getImage()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
