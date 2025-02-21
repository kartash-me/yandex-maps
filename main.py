import os
import sys

from request import get_map

from PyQt6 import uic
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow


class Map(QMainWindow):
    def __init__(self):
        super().__init__(None)
        self.longitude = 37.620070
        self.latitude = 55.753630
        self.z = 20
        self.theme = "light"

        with open("files/light.qss") as light, open("files/dark.qss") as dark:
            self.qss = {"light": light.read(), "dark": dark.read()}

        self.initUI()
        self.update_map()

    def initUI(self):
        uic.loadUi("files/ui.ui", self)
        self.setStyleSheet(self.qss.get(self.theme))
        self.setWindowTitle("Yandex Maps API")
        self.setFixedSize(800, 450)

        self.light.setIcon(QIcon("files/light.png"))
        self.light.setIconSize(QSize(50, 50))
        self.light.clicked.connect(self.change_theme)
        self.light.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.dark.setIcon(QIcon("files/dark.png"))
        self.dark.setIconSize(QSize(45, 45))
        self.dark.clicked.connect(self.change_theme)
        self.dark.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def show_map(self):
        if os.path.isfile("map.png"):
            image = QPixmap("map.png")
            self.label.setPixmap(image)
            os.remove("map.png")
        else:
            self.label.setText("ИНВАЛИД РЕКВЕСТ")

    def keyPressEvent(self, event, **kwargs):
        key = str(event.key())
        # print(f"кнопка: {key}")

        if key == "16777239": # page down
            self.z = max(0, min(self.z - 1, 21))
        elif key == "16777238": # page up
            self.z = max(0, min(self.z + 1, 21))
        elif key == "16777235": # up
            self.longitude = max(-180.0, min(180.0, self.longitude + 0.0))
            self.latitude = max(-85.0, min(85.0, self.latitude + 0.0003 * (22 - self.z)))
        elif key == "16777234": # left
            self.longitude = max(-180.0, min(180.0, self.longitude - 0.0003 * (22 - self.z)))
            self.latitude = max(-85.0, min(85.0, self.latitude + 0.0))
        elif key == "16777237": # down
            self.longitude = max(-180.0, min(180.0, self.longitude + 0.0))
            self.latitude = max(-85.0, min(85.0, self.latitude - 0.0003 * (22 - self.z)))
        elif key == "16777236": # right
            self.longitude = max(-180.0, min(180.0, self.longitude + 0.0003 * (22 - self.z)))
            self.latitude = max(-85.0, min(85.0, self.latitude + 0.0))

        self.update_map()

    def update_map(self):
        if get_map(self.z, self.longitude, self.latitude, self.theme):
            self.show_map()
        else:
            self.label.setText("ИНВАЛИД РЕКВЕСТ")

    def change_theme(self):
        self.theme = self.sender().objectName()
        self.setStyleSheet(self.qss.get(self.theme))
        self.update_map()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    yandex_map = Map()
    yandex_map.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
