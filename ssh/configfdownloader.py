#!/usr/bin/python3
import termcolor

class ConfigDownloader(object):
    def __init__(self, address, username, password, commands):
        import paramiko
        self.commands = commands
        self.username = username
        self.password = password
        self.address = address
        self.conn = paramiko.SSHClient()
        self.conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.shell = None

    def download(self):
        from paramiko.ssh_exception import AuthenticationException

        def send_and_readuntil(message, until):
            self.shell.send(message)
            temp = b""
            out = b""
            while until.encode() not in temp:
                temp = self.shell.recv(4096)
                out += temp
            return out

        self.commands = ["show run"]
        try:
            self.conn.connect(self.address, 22, username=self.username,
                              password=self.password, timeout=5, allow_agent=False, look_for_keys=False)
        except AuthenticationException:
            print(termcolor.colored(
                f"Authentication failed for {self.address}", 'red'))
            return ""

        self.shell = self.conn.invoke_shell()
        self.shell.settimeout(2)
        self.shell.setblocking(1)

        send_and_readuntil("enable\n", "Password:")
        send_and_readuntil(self.password + "\n", "#")
        send_and_readuntil("terminal length 0\n", "#")

        configs = ""
        for command in self.commands:
            config = send_and_readuntil(command + "\n", "#").decode()
            configs += config[:config.rfind('\n')]

        self.shell.send("terminal length 24\n")
        self.shell.close()
        return configs