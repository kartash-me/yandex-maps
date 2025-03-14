import os
import sys

from PyQt6 import uic
from PyQt6.QtCore import QEvent, QSize, Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit

from request import geocode, get_map


class Map(QMainWindow):
    def __init__(self):
        super().__init__(None)
        self.longitude = 37.619881
        self.latitude = 55.753674
        self.z = 20
        self.theme = "light"
        self.marker = self.index = self.address = None

        with open("files/light.qss") as light, open("files/dark.qss") as dark:
            self.qss = {"light": light.read(), "dark": dark.read()}

        self.initUI()
        self.update_map()

    def initUI(self):
        uic.loadUi("files/ui.ui", self)
        self.setStyleSheet(self.qss.get(self.theme))
        self.setWindowTitle("Yandex Maps API")
        self.setFixedSize(800, 470)

        self.search_button.clicked.connect(self.search_object)
        self.search_result.setReadOnly(True)
        self.search_result.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self.index_checkbox.stateChanged.connect(self.show_address)
        self.reset_button.clicked.connect(self.reset_object)
        self.search_req.returnPressed.connect(self.search_object)
        self.search_req.installEventFilter(self)

        for btn in (self.light, self.dark):
            btn.setIcon(QIcon(f"files/{btn.objectName()}.png"))
            btn.setIconSize(QSize(45, 45))
            btn.clicked.connect(self.change_theme)
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.KeyPress and source is self.search_req:
            key = event.key()

            if key in (Qt.Key.Key_Left, Qt.Key.Key_Right,
                       Qt.Key.Key_Up, Qt.Key.Key_Down,
                       Qt.Key.Key_PageUp, Qt.Key.Key_PageDown):
                self.keyPressEvent(event)
                return True

        return super().eventFilter(source, event)

    def search_object(self):
        query = self.search_req.text().strip()
        self.search_req.setText("")

        if not query:
            self.statusBar().showMessage("Введите запрос")
            return

        longitude, latitude, address, self.index = geocode(query)

        if None in (longitude, latitude, address):
            self.statusBar().showMessage("Объект не найден")
            return

        self.marker = self.longitude, self.latitude = longitude, latitude
        self.address = address
        self.show_address()
        self.update_map()

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key.Key_PageDown:
            self.z = max(0, min(self.z - 1, 21))
        elif key == Qt.Key.Key_PageUp:
            self.z = max(0, min(self.z + 1, 21))
        elif key == Qt.Key.Key_Up:
            self.latitude = max(-85.0, min(85.0, self.latitude + 0.0001 * (22 - self.z)))
        elif key == Qt.Key.Key_Left:
            self.longitude = max(-180.0, min(180.0, self.longitude - 0.0001 * (22 - self.z)))
        elif key == Qt.Key.Key_Down:
            self.latitude = max(-85.0, min(85.0, self.latitude - 0.0001 * (22 - self.z)))
        elif key == Qt.Key.Key_Right:
            self.longitude = max(-180.0, min(180.0, self.longitude + 0.0001 * (22 - self.z)))

        self.update_map()

    def update_map(self):
        if get_map(self.z, self.longitude, self.latitude, self.theme, self.marker) and os.path.exists("map.png"):
            self.label.setPixmap(QPixmap("map.png"))
            os.remove("map.png")
        else:
            self.statusBar().showMessage("Ошибка получения карты")

    def change_theme(self):
        self.theme = self.sender().objectName()
        self.setStyleSheet(self.qss.get(self.theme))
        self.update_map()

    def show_address(self):
        self.statusBar().showMessage("")

        if self.address:
            if self.index_checkbox.isChecked():
                if self.index:
                    self.search_result.setText(f"{self.index}, {self.address}")
                else:
                    self.search_result.setText(self.address)
                    self.statusBar().showMessage("Индекс не найден")
            else:
                self.search_result.setText(self.address)

    def reset_object(self):
        if self.marker:
            self.marker = self.index = self.address = None
            self.update_map()
            self.search_result.setText("")
        else:
            self.statusBar().showMessage("На карте нет маркера")


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("files/logo.png"))

    yandex_map = Map()
    yandex_map.show()

    sys.excepthook = except_hook
    sys.exit(app.exec())
