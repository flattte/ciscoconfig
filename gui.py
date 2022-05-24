from ping3 import ping
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import *
from functools import partial
from parser.parserutils import is_ip_valid
from ssh.configfdownloader import ConfigDownloader
from parser.strictmatching import StrictMatchingParser
from parser.parserutils import open_files
import sys
import ipaddress
import logging
import threading
import time
import datetime
logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.INFO)
# main windows class
logging.info(f'Started logging {datetime.datetime.now()}')


class myQlineEdit(QLineEdit):
    def __init__(self, I, J, parent=None):
        super(myQlineEdit, self).__init__(parent)
        self.setPlaceholderText("Enter IP Address")
        self.textChanged.connect(self.onTextChanged)

    def onTextChanged(self):
        text = self.text()
        if text == "":
            self.setStyleSheet("background-color: white")
        else:
            if is_ip_valid(text):
                self.setStyleSheet("background-color: green")
            else:
                self.setStyleSheet("background-color: red")


class Window:
    def __init__(self):
        self.box_list = []
        self.ping_func = []
        self.ssh_func = []
        self.addresses = dict()
        self.app = QApplication(sys.argv)
        self.win = QWidget()
        self.grid = QGridLayout()
        for i in range(0, 8):
            for j in range(0, 2):
                j *= 5
                box = myQlineEdit(i, j)
                box.setPlaceholderText("Enter IP Address")
                box.resize(200, 30)
                box.textEdited.connect(lambda: box.onTextChanged())
                self.box_list.append(box)
                self.grid.addWidget(box, i, j)

                button = QPushButton("SSH", self.win)
                handler = partial(self.buttonSSH, button, box)
                button.clicked.connect(handler)
                self.grid.addWidget(button, i, j+1)
                self.ssh_func.append(handler)

                button = QPushButton("PING", self.win)
                handler = partial(self.buttonPing, button, box)
                button.clicked.connect(handler)
                self.grid.addWidget(button, i, j+2)
                self.ping_func.append(handler)

        self.win.setLayout(self.grid)
        self.win.setMinimumSize(QSize(800, 600))
        self.win.setWindowTitle("PyQt")
        self.win.show()

        x = threading.Thread(target=self.ping_devices)
        x.daemon = True
        x.start()

        x = threading.Thread(target=self.try_ssh)
        x.daemon = True
        x.start()

        app = self.app.exec()
        self.finish()
        sys.exit(app)

    def ping_devices(self):
        while True:
            logging.info("pinging devices")
            for f in self.ping_func:
                f()
            time.sleep(10)

    def try_ssh(self):
        logging.info("checking ssh connection")
        while True:
            for f in self.ssh_func:
                f()
            time.sleep(30)

    def buttonSSH(self, button, box):
        ip = box.text()
        if ip == "":
            button.setStyleSheet("background-color: lightGrey")
            return
        if is_ip_valid(ip):
            ssh = ConfigDownloader(ip, "cisco", "cisco", None)
            if ssh.check():
                logging.info(f"{ip} ssh ok")
                button.setStyleSheet("background-color: green")
                return
            else:
                logging.info(f"{ip} ssh failed")
                button.setStyleSheet("background-color: red")
                return
        else:
            button.setStyleSheet("background-color: lightGrey")
            return

    def buttonPing(self, button, box):
        ip = box.text()
        if ip == "":
            button.setStyleSheet("background-color: lightGrey")
            return

        if is_ip_valid(ip):
            if ping(ip):
                logging.info(f"{ip} ping ok")
                button.setStyleSheet("background-color: green")
                return
            else:
                logging.info(f"{ip} ping failed")
                button.setStyleSheet("background-color: red")
                return
        else:
            button.setStyleSheet("background-color: lightGrey")
            return

    def finish(self):
        for box in self.box_list:
            ip = box.text()
            if is_ip_valid(ip):
                downloader = ConfigDownloader(
                    ip, "cisco", "cisco", ["show run", "show vlan"])
                with open(f"results/config_{ip}.txt", 'w') as f:
                    f.write(downloader.download())
                logging.info(f"{ip} config downloaded")

                verbose = True
                config, target = open_files(
                    "test/cfg.txt", f"results/config_{ip}.txt")
                parser = StrictMatchingParser(config, target, verbose)
                parser.parse()
                with open(f"results/result_{ip}.txt", 'w') as f:
                    f.write(
                        f"Matches found {parser.score} out of {parser.n_of_tokens}")
                logging.info(f"{ip} config parsed")


win = Window()
