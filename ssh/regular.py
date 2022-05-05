from paramiko import SSHClient, AutoAddPolicy


class SSHCisco(object):
    def __init__(self):
        self.conn = SSHClient()
        self.conn.set_missing_host_key_policy(AutoAddPolicy())
        self.PASSWORD = "cisco"
        self.CONFIG = "show run"
        self.connected = False

    def __del__(self):
        self.conn.close()

    
    def connect(self, ip, user, passw):
        try:
            self.conn.connect(ip, 22, username=user, password=passw, timeout=5)  
            self.conn.connected = True
        except Exception:
            print("not able to connect with ssh")
            self.connected = False

        self.shell = self.conn.invoke_shell()
        self.shell.settimeout(2)
        self.shell.setblocking(1)


    def readConfig(self):
        self.send_and_readuntil(self.shell,"enable\n","Password:")
        self.send_and_readuntil(self.shell,PASSWORD+"\n","#")
        self.send_and_readuntil(self.shell,"terminal length 0\n","#")
        config = self.send_and_readuntil(self.shell, CONFIG + "\n","#")
        self.shell.send("terminal length 24\n")
        self.shell.close()
        return config.decode()
    

    @staticmethod
    def send_and_readuntil(shell, message, until):
        shell.send(message)
        temp = b""
        out = b""
        while until.encode() not in temp:
            temp = shell.recv(4096)
            out += temp
        return out  


    @property
    def isConnected(self):
    	return self.connected
