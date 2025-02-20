import os
import sys

from request import get_map
from PyQt6 import uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow


class Map(QMainWindow):
    def __init__(self):
        super().__init__(None)
        self.label = None
        uic.loadUi("ui.ui", self)
        self.setCentralWidget(self.label)
        self.longitude = 37.620070
        self.latitude = 55.753630
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
        #print(f"кнопка: {key}")
        if key == "16777239":
            self.update_map(z=-1)
        elif key == "16777238":
            self.update_map(z=1)
        elif key == "16777235": #up
            self.longitude = max(-180.0, min(180.0, self.longitude + 0.0))
            self.latitude = max(-85.0, min(85.0, self.latitude + 0.0003))
        elif key == "16777234": #left
            self.longitude = max(-180.0, min(180.0, self.longitude - 0.0003))
            self.latitude = max(-85.0, min(85.0, self.latitude + 0.0))
        elif key == "16777237": #down
            self.longitude = max(-180.0, min(180.0, self.longitude + 0.0))
            self.latitude = max(-85.0, min(85.0, self.latitude - 0.0003))
        elif key == "16777236": #right
            self.longitude = max(-180.0, min(180.0, self.longitude + 0.0003))
            self.latitude = max(-85.0, min(85.0, self.latitude + 0.0))
        self.update_map()

    def update_map(self, z=0):
        if 0 <= self.z + z <= 21:
            self.z += z

        if get_map(self.z, self.longitude, self.latitude):
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
    
