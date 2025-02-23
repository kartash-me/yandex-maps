import sys

from request import *

from PyQt6 import uic
from PyQt6.QtCore import QSize, Qt, QEvent
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow


class Map(QMainWindow):
    def __init__(self):
        super().__init__(None)
        self.longitude = 37.619881
        self.latitude = 55.753674
        self.z = 20
        self.theme = "light"
        self.marker = None

        with open("files/light.qss") as light, open("files/dark.qss") as dark:
            self.qss = {"light": light.read(), "dark": dark.read()}

        self.initUI()
        self.update_map()

    def initUI(self):
        uic.loadUi("files/ui.ui", self)
        self.setStyleSheet(self.qss.get(self.theme))
        self.setWindowTitle("Yandex Maps API")
        self.setFixedSize(800, 450)
        self.search_button.clicked.connect(self.search_object)
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
        if not query:
            self.statusBar().showMessage("Введите запрос")
            return

        longitude, latitude, address = geocode(query)

        if None in (longitude, latitude, address):
            self.statusBar().showMessage("Объект не найден")
            return

        self.longitude = longitude
        self.latitude = latitude
        self.marker = (longitude, latitude)

        self.statusBar().showMessage(f"Найдено: {address}")
        self.update_map()

    def show_map(self):
        if os.path.isfile("map.png"):
            image = QPixmap("map.png")
            self.label.setPixmap(image)
            os.remove("map.png")
        else:
            self.label.setText("ИНВАЛИД РЕКВЕСТ")

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key.Key_PageDown:  # page down
            self.z = max(0, min(self.z - 1, 21))
        elif key == Qt.Key.Key_PageUp:  # page up
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
        if get_map(self.z, self.longitude, self.latitude, self.theme, pt=self.marker):
            self.show_map()
        else:
            self.label.setText("ИНВАЛИД РЕКВЕСТ")

    def change_theme(self):
        self.theme = self.sender().objectName()
        self.setStyleSheet(self.qss.get(self.theme))
        self.update_map()

    def reset_object(self):
        if self.marker:
            self.marker = None
            self.update_map()
        else:
            self.statusBar().showMessage("На карте нету маркера")


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("files/logo.png"))

    yandex_map = Map()
    yandex_map.show()

    sys.excepthook = except_hook
    sys.exit(app.exec())
