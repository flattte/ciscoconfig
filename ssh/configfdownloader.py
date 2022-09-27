#!/usr/bin/python3
from functools import cache
from typing import List
import paramiko
import time

class ConfigDownloader(object):
    def __init__(self, address, username, password, priv_exec_mode, commands):
        self.commands: List[str] = commands
        self.username: str = username
        self.password: str = password
        self.priv_exec_mode: str = priv_exec_mode
        self.address: str = address
        self.conn: paramiko.SSHClient = paramiko.SSHClient()
        self.conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.shell: paramiko.Channel | None = None

    def check(self) -> bool:
        try:
            self.conn.connect(self.address, 22, username=self.username,
                              password=self.password, timeout=5, allow_agent=False, look_for_keys=False)
        except:
            return False
        return True

    def download(self) -> str:
        def send_and_readuntil(message, until):
            self.shell.send(message)
            temp: bytes = b""
            out: bytes = b""
            while until.encode() not in temp:
                temp = self.shell.recv(4096)
                out += temp
            return out

        try:
            self.conn.connect(self.address, 22, username=self.username,
                              password=self.password, timeout=5, allow_agent=False, look_for_keys=False)
        except:
            print(f"Authentication failed for {self.address}")
            return ""

        self.shell = self.conn.invoke_shell()
        self.shell.settimeout(2)
        self.shell.setblocking(1)
        time.sleep(0.4)
        if self.shell.recv(100)[-1] == b'#':
            print("enable")
            send_and_readuntil("enable\n", "Password:")
            send_and_readuntil(self.priv_exec_mode + "\n", "#")
        send_and_readuntil("terminal length 0\n", "#")

        configs = ""
        for command in self.commands:
            config = send_and_readuntil(command + "\n", "#").decode()
            configs += config[:config.rfind('\n')]

        self.shell.send(b"terminal length 24\n")
        self.shell.close()
        return configs
