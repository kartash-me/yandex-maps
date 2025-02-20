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
        get_map()
        self.show_map()

    def show_map(self):
        map = QPixmap("map.png")
        self.label.setPixmap(map)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    map = Map()
    map.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
