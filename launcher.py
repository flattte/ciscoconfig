#!/usr/bin/env python3
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QLineEdit, QApplication, QWidget, QPushButton, QFormLayout, QMessageBox
import sys
import os
MAX_SIZE = 17


class EntryMenu(QWidget):
    def __init__(self):
        self.app = QApplication([])
        super(QWidget, self).__init__()
        self.boxes = []
        self.setWindowTitle("Ciscoconfig")
        self.text_boxes = (("config file", "test/cfg.txt"), ("ssh username", "admin"), ("ssh password", "cisco"),
                           ("priv exec mode", "class"))
        for (text, default) in self.text_boxes:
            box = QLineEdit()
            box.setPlaceholderText(f"{text} or default: {default}")
            self.boxes.append(box)

        self.cbox = QLineEdit()
        self.cbox.setPlaceholderText("columns")
        self.cbox.textChanged.connect(self.onTextChanged)

        self.rbox = QLineEdit()
        self.rbox.setPlaceholderText("rows")
        self.rbox.textChanged.connect(self.onTextChanged)

        okButton = QPushButton("OK", self)
        okButton.clicked.connect(self.validate)

        layout = QFormLayout()
        for box in self.boxes:
            layout.addRow(box)
        layout.addWidget(self.rbox)
        layout.addWidget(self.cbox)
        layout.addWidget(okButton)
        self.setMinimumSize(360, 250)
        self.setLayout(layout)
        self.show()

    def onTextChanged(self):
        self.columns = self.cbox.text()
        self.rows = self.rbox.text()

    def validate(self):
        def popErr(text):
            msg = QMessageBox()
            msg.setWindowTitle("")
            msg.setText("Wrong arguments: " + text)
            x = msg.exec()
        try:
            self.columns = int(self.columns)
            self.rows = int(self.rows)
        except (ValueError, TypeError):
            popErr("Entry must be a number.")
            return
        except Exception as e:
            popErr("Entry must be a number.")
            return

        if any(x > MAX_SIZE or x < 0 for x in (self.columns, self.rows)):
            popErr(
                f"Numbers are preferably positive, and smaller than {MAX_SIZE}")
            return
        else:
            self.close()


def main():
    entry = EntryMenu()
    app = entry.app.exec()
    try:
        columns = int(entry.columns)
        rows = int(entry.rows)
    except:
        sys.exit()

    for i in range(len(entry.boxes)):
        box = entry.boxes[i]
        if not box.text():
            box.setText(entry.text_boxes[i][1])
    config_file = entry.boxes[0].text()
    ssh_username = entry.boxes[1].text()
    ssh_password = entry.boxes[2].text()
    priv_exec_mode = entry.boxes[3].text()
    rows = entry.rows
    columns = entry.columns
    if any(x > MAX_SIZE or x <= 0 for x in (rows, columns)):
        sys.exit()
    command = f"{sys.executable} gui.py -f {config_file} -u {ssh_username} -p {ssh_password} -e {priv_exec_mode} -r {rows} -c {columns}"
    with open("lastrun","w") as f:
        f.write(command)
    os.system(command)
    sys.exit()

if __name__ == "__main__":
    main()