import os
import sys

from request import get_map
from PyQt6 import uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow


class Map(QMainWindow):
    def __init__(self):
        super().__init__(None)
        uic.loadUi("ui.ui", self)
        self.setCentralWidget(self.label)
        self.z = 20
        self.update_map()

    def show_map(self):
        if os.path.isfile("map.png"):
            map = QPixmap("map.png")
            self.label.setPixmap(map)
            os.remove("map.png")
        else:
            self.label.setText("ИНВАЛИД РЕКВЕСТ")

    def keyPressEvent(self, event):
        key = str(event.key())

        if key == "16777239":
            self.update_map(z=-1)
        elif key == "16777238":
            self.update_map(z=1)

    def update_map(self, z=0):
        if 0 <= self.z + z <= 21:
            self.z += z

        if get_map(self.z):
            self.show_map()
        else:
            self.label.setText("ИНВАЛИД РЕКВЕСТ")


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    map = Map()
    map.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
