#!/usr/bin/env python3
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QLineEdit, QApplication, QWidget, QPushButton, QFormLayout, QMessageBox
from parser.parserutils import parse_args
import sys
import os
MAX_SIZE = 17


def popErr(text):
    msg = QMessageBox()
    msg.setWindowTitle("")
    msg.setText(text)
    x = msg.exec()


class EntryMenu(QWidget):
    def __init__(self):
        self.app = QApplication([])
        self.columns = ""
        self.rows = ""
        super(QWidget, self).__init__()
        self.boxes = dict()
        self.setWindowTitle("Ciscoconfig")
        text_boxes = {"config file": "test/cfg.txt", "ssh username": "admin", "ssh password": "cisco",
                      "priv exec mode": "class"}
        for text in text_boxes:
            box = QLineEdit()
            box.setPlaceholderText(f"{text} or default: {text_boxes[text]}")
            self.boxes[box] = (text_boxes[text])

        self.cbox = QLineEdit()
        self.cbox.setPlaceholderText("Columns")
        self.cbox.textChanged.connect(self.onTextChanged)

        self.rbox = QLineEdit()
        self.rbox.setPlaceholderText("Rows")
        self.rbox.textChanged.connect(self.onTextChanged)

        okButton = QPushButton("OK", self)
        okButton.clicked.connect(self.validate)

        lastrunButton = QPushButton("Last run", self)
        lastrunButton.clicked.connect(self.lastrun)

        layout = QFormLayout()
        for box in self.boxes:
            layout.addRow(box)
        layout.addWidget(self.rbox)
        layout.addWidget(self.cbox)
        layout.addWidget(okButton)
        layout.addWidget(lastrunButton)
        self.setMinimumSize(360, 250)
        self.setLayout(layout)
        self.show()

    def lastrun(self):
        try:
            with open("lastrun") as f:
                command = f.read()
                args = parse_args(command.split(" ")[2:])
                boxes = list(self.boxes.keys())
                boxes[0].setText(args.config_file)
                boxes[1].setText(args.username)
                boxes[2].setText(args.password)
                boxes[3].setText(args.priv_exec_mode)
                self.cbox.setText(args.columns)
                self.rbox.setText(args.rows)
        except Exception as e:
            popErr(f"Error: {e}")

    def onTextChanged(self):
        self.columns = self.cbox.text()
        self.rows = self.rbox.text()

    def validate(self):
        rows = self.check_int(self.rows)
        if not rows:
            popErr(f"\"{self.rows}\" is not a number")
            return
        columns = self.check_int(self.columns)
        if not columns:
            popErr(f"\"{self.columns}\" is not a number")
            return

        if any(x > MAX_SIZE or x < 0 for x in (columns, rows)):
            popErr(
                f"Numbers are preferably positive, and smaller than {MAX_SIZE}")
            return
        else:
            self.close()

    def check_int(self, str):
        try:
            integer = int(str)
        except (ValueError, TypeError):
            return None
        return integer


def launcherMenu():
    entry = EntryMenu()
    app = entry.app.exec()
    try:
        columns = int(entry.columns)
        rows = int(entry.rows)
    except:
        sys.exit()
    if any(x > MAX_SIZE or x < 0 for x in (columns, rows)):
        sys.exit()

    args = list(entry.boxes.values())
    for n, box in enumerate(entry.boxes):
        if box.text():
            args[n] = box.text()

    command = f"{sys.executable} gui.py -f {args[0]} -u {args[1]} -p {args[2]} -e {args[3]} -r {entry.rows} -c {entry.columns}"
    with open("lastrun", "w") as f:
        f.write(command)

    return args, entry.rows, entry.columns