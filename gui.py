from ping3 import ping
import sys
import ipaddress
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import *
from functools import partial
import asyncio
import datetime
from parser.parserutils import is_ip_valid

# main windows class
class myQlineEdit(QLineEdit):
    def __init__(self, I, J, parent=None):
        super(myQlineEdit, self).__init__(parent)
        self.setPlaceholderText("Enter IP Address")
        self.textChanged.connect(self.onTextChanged)

    def onTextChanged(self):
        text = self.text()

        try:
            ipaddress.ip_address(text)
            self.setStyleSheet("background-color: green")
        except:
            self.setStyleSheet("background-color: red")
            if text == "":
                self.setStyleSheet("background-color: white")

    def __del__(self):
        print("Destructor called")


class Window:
    def __init__(self):
        self.box_list = []
        self.addresses = dict()
        self.app = QApplication(sys.argv)
        self.win = QWidget()
        self.grid = QGridLayout()
        for i in range(0, 8):
            for j in range(0, 2):
                j *= 5
                box = myQlineEdit(i, j)
                box.setPlaceholderText("Enter IP Address")
                box.move(0, 30)
                box.resize(200, 30)
                box.textEdited.connect(lambda: box.onTextChanged())
                self.box_list.append(box)
                self.grid.addWidget(box, i, j)

                checkbox = QCheckBox("")
                checkbox.setDisabled(True)
                checkbox.resize(30, 30)
                self.grid.addWidget(checkbox, i, j+1)

                button = QPushButton("SSH", self.win)
                handler = partial(self.buttonSSH, checkbox, box)
                button.clicked.connect(handler)
                button.resize(30, 30)
                self.grid.addWidget(button, i, j+3)

                checkbox = QCheckBox("")
                checkbox.setDisabled(True)
                print(checkbox.styleSheet())
                checkbox.resize(30, 30)
                self.grid.addWidget(checkbox, i, j+2)

                button = QPushButton("PING", self.win)
                handler = partial(self.buttonPing, checkbox, box)
                button.clicked.connect(handler)
                self.grid.addWidget(button, i, j+4)

        self.win.setLayout(self.grid)
        self.win.setMinimumSize(QSize(800, 600))
        self.win.setWindowTitle("PyQt")
        self.win.show()
        sys.exit(self.app.exec())

    def buttonSSH(self, checkbox, vcv):
        address = vcv.text()

    def buttonPing(self, checkbox, box):
        ip = box.text()
        if ip == "":
            checkbox.setStyleSheet("background-color: lightGrey")
            return

        if is_ip_valid(ip):
            if ping(ip):
                print("ping ok")
                checkbox.setStyleSheet("background-color: green")
                return
            else:
                print("ping failed")
                checkbox.setStyleSheet("background-color: red")
                return
        else:
            checkbox.setStyleSheet("background-color: lightGrey")
            return


win = Window()
