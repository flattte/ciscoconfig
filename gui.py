from ping3 import ping
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QLineEdit, QApplication, QWidget, QPushButton, QGridLayout
from functools import partial
from parser.parserutils import is_ip_valid
from ssh.configfdownloader import ConfigDownloader
from parser.strictmatching import StrictMatchingParser
from parser.parserutils import open_files
import argparse
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

# main windows class


class Window:
    def __init__(self, rows, columns, ssh_creds):
        self.box_list = []
        self.ping_func = []
        self.ssh_func = []
        self.ssh_creds = ssh_creds
        self.addresses = dict()
        self.app = QApplication(sys.argv)
        self.win = QWidget()
        self.win.setWindowTitle("ciscoconfig")
        self.grid = QGridLayout()
        for i in range(0, rows):
            for j in range(0, columns):
                j *= 3
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

    def finish(self, config_file):
        for box in self.box_list:
            ip = box.text()
            if is_ip_valid(ip):
                downloader = ConfigDownloader(
                    ip, ssh_creds.username, ssh_creds.password, ssh_creds.priv_exec_mode, ["show run", "show vlan"])
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
    arg_parser = argparse.ArgumentParser(description="main gui for ciscoconfig",
                                         usage=f"{sys.executable} {sys.argv[0]} -f <path to config file> -u <ssh username> -p <ssh password> -e <privileged exec mode password> -r <rows> -c <columns>")
    arg_parser.add_argument('-f', dest='config_file',
                            help='path to config file.')
    arg_parser.add_argument('-u', dest='username', help='ssh username')
    arg_parser.add_argument('-p', dest='password', help='ssh password')
    arg_parser.add_argument('-e', dest='priv_exec_mode',
                            help='password for privileged exec mode')
    arg_parser.add_argument('-r', dest='rows', help='number of rows')
    arg_parser.add_argument('-c', dest='columns', help='number of columns')
    args = arg_parser.parse_args()

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
