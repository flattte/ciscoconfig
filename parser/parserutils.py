import os
import termcolor

def tokenizeConfig(config) -> list():
    token, tokens = [], []
    for line in config.read().splitlines():
        if '!' in line:
            if token: tokens.append(token)
            token = []
        else:
            token.append(line.strip("\t ").strip(" "))

    return tokens

def tokenizeTarget(target) -> list():
    token, tokens = [], []
    for line in target.read().splitlines():
        if '!' in line:
            if token: tokens.append(token)
            token = []
        else:
            token.append(line.strip("\t ").strip(" "))
    return tokens

def yieldToken(token):
    yield token[1][1]
    for t in token[1][0]:
        yield t
    
    
def printToken(token, color="white") -> None:
    if os.name == "nt":
        os.system("color")
    g = yieldToken(token)
    print("Query:")
    print(termcolor.colored(f"    {next(g)}", color))
    print("Body:")
    [print(termcolor.colored(f"    {next(g)}", color)) for _ in range(len(token[1][0]))]
    print()

def open_files(path1, path2):
    assert type(path1) is str, "Enter a -s flag followed by config path to config file."
    assert type(path2) is str, "Enter a -t flag followed by config path to config file."
    try:
        file1 = open(path1, 'r')
    except Exception as e:
        exit(f"Exception {e.__class__} occurred while opening {path1}. \n Enter a valid path to a file that exists")

    try:
        file2 = open(path2, 'r')
    except Exception as e:
        exit(f"Exception {e.__class__} occurred while opening {path2}. \n Enter a valid path to a file that exists")

    return file1, file2

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
        def send_and_readuntil(message, until):
            self.shell.send(message)
            temp = b""
            out = b""
            while until.encode() not in temp:
                temp = self.shell.recv(4096)
                out += temp
            return out

        self.commands = ["show run"]

        self.conn.connect(self.address, 22, username=self.username,
                          password=self.password, timeout=5)

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
