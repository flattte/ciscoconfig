import time
import paramiko


PASSWORD = "cisco"
CONFIG = "show run"


def send_and_readuntil(shell,message,until):
	shell.send(message)
	temp = b""
	out = b""
	while until.encode() not in temp:
		temp = shell.recv(4096)
		out += temp
	return out

conn = paramiko.SSHClient()
conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())

conn.connect("192.168.43.32", 22, username="cisco", password="cisco", timeout=5)
shell = conn.invoke_shell()
shell.settimeout(2)
shell.setblocking(1)

send_and_readuntil(shell,"enable\n","Password:")
send_and_readuntil(shell,PASSWORD+"\n","#")
send_and_readuntil(shell,"terminal length 0\n","#")

config = send_and_readuntil(shell, CONFIG + "\n","#")


shell.send("terminal length 24\n")
shell.close()


print(config.decode())
