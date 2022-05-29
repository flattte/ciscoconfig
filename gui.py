from ping3 import ping
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QLineEdit, QApplication, QWidget, QPushButton, QGridLayout, QGroupBox
from functools import partial
from parser.parserutils import is_ip_valid
from ssh.configfdownloader import ConfigDownloader
from parser.strictmatching import StrictMatchingParser
from parser.parserutils import open_files, parse_args
import sys
import time
import logging
import threading
import datetime

class SSH_creds:
    def __init__(self, username, password, priv_exec_mode):
        self.username = username
        self.password = password
        self.priv_exec_mode = priv_exec_mode


class myQlineEdit(QLineEdit):
    def __init__(self, parent=None):
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

class DesktopComponent(QGroupBox):
    def __init__(self, id, devices_list, parent_ref, parent=None):
        super(DesktopComponent, self).__init__()
        self.setTitle(str(id))
        self.parent_ref = parent_ref
        self.devices_list = devices_list
        self.layout = QGridLayout()
        for i in range(len(self.devices_list)):
            self.initDevice(self.devices_list[i], i)

    def initDevice(self, device, row):
        box = myQlineEdit()
        box.setPlaceholderText(f"Enter {device} ip address")
        box.resize(200, 30)
        box.textEdited.connect(lambda: box.onTextChanged)
        self.parent_ref.box_list.append(box)
        self.layout.addWidget(box, row, 0)

        button = QPushButton("SSH")
        handler = partial(self.buttonSSH, button, box)
        button.clicked.connect(handler)
        self.parent_ref.ssh_func.append(handler)
        self.layout.addWidget(button, row, 1)

        button = QPushButton("PING")
        handler = partial(self.buttonPing, button, box)
        button.clicked.connect(handler)
        self.parent_ref.ping_func.append(handler)
        self.layout.addWidget(button, row, 2)
        self.setLayout(self.layout)

    def buttonSSH(self, button, box):
        ip = box.text()
        if ip == "":
            button.setStyleSheet("background-color: lightGrey")
            return
        if is_ip_valid(ip):
            ssh = ConfigDownloader(
                ip, ssh_creds.username, ssh_creds.password, ssh_creds.priv_exec_mode, None)
            if ssh.check():
                logging.info(f"{datetime.datetime.now()} {ip} ssh ok")
                button.setStyleSheet("background-color: green")
                return
            else:
                logging.info(f"{datetime.datetime.now()} {ip} ssh failed")
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
            pg = ping(ip)
            if pg or pg == 0.0:
                logging.info(f"{datetime.datetime.now()} {ip} ping ok")
                button.setStyleSheet("background-color: green")
                return
            else:
                logging.info(f"{datetime.datetime.now()} {ip} ping failed")
                button.setStyleSheet("background-color: red")
                return
        else:
            button.setStyleSheet("background-color: yellow")
            return

class Window:
    def __init__(self, rows, columns, ssh_creds):
        self.box_list = []
        self.ping_func = []
        self.ssh_func = []
        self.ssh_creds = ssh_creds
        self.app = QApplication(sys.argv)
        self.win = QWidget()
        self.win.setWindowTitle("ciscoconfig")
        self.grid = QGridLayout()
        devices_list = ["R1", "R2", "S1", "S2"]

        for i in range(rows):
            for j in range(columns):
                id = i*columns + j
                desktop = DesktopComponent(id, devices_list, self)
                self.grid.addWidget(desktop, i, j)

        self.win.setLayout(self.grid)
        self.win.setMinimumSize(QSize(800, 600))
        self.win.setWindowTitle("CiscoConfig")
        self.win.show()

        x = threading.Thread(target=self.ping_devices)
        x.daemon = True
        x.start()

        x = threading.Thread(target=self.try_ssh)
        x.daemon = True
        x.start()

    def ping_devices(self):
        while True:
            logging.info("{datetime.datetime.now()} pinging devices")
            for f in self.ping_func:
                f()
            time.sleep(10)

    def try_ssh(self):
        logging.info("{datetime.datetime.now()} checking ssh connection")
        while True:
            for f in self.ssh_func:
                f()
            time.sleep(30)

    def finish(self, config_file):
        for box in self.box_list:
            ip = box.text()
            if is_ip_valid(ip):
                downloader = ConfigDownloader(
                    ip, ssh_creds.username, ssh_creds.password, ssh_creds.priv_exec_mode, ("show run", "show vlan"))
                with open(f"results/config_{ip}.txt", 'w') as f:
                    f.write(downloader.download())
                logging.info(
                    f"{datetime.datetime.now()} {ip} config downloaded")

                verbose = True
                config, target = open_files(
                    config_file, f"results/config_{ip}.txt")
                parser = StrictMatchingParser(config, target, verbose)
                parser.parse()
                with open(f"results/result_{ip}.txt", 'w') as f:
                    f.write(
                        f"Matches found {parser.score} out of {parser.n_of_tokens}")
                logging.info(f"{datetime.datetime.now()} {ip} config parsed")


if __name__ == "__main__":
    # python gui.py -f test/cfg.txt -u cisco -p cisco -e cisco -r 4 -c 2
    args = parse_args(None)

    logging.basicConfig(filename='app.log',
                        encoding='utf-8', level=logging.INFO)
    logging.info(f'{datetime.datetime.now()} Started logging')
    ssh_creds = SSH_creds(args.username, args.password, args.priv_exec_mode)

    columns = int(args.columns)
    rows = int(args.rows)
    win = Window(rows, columns, ssh_creds)
    app = win.app.exec()
    win.finish(args.config_file)
    sys.exit(app)
