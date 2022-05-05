#!/usr/bin/python3
from parser.strictmatching import StrictMatchingParser
from parser.parserutils import open_files
from ssh.regular import SSHCisco




if __name__ == "__main__":

    verbose = True
    config, target = open_files("test/cfg.txt", "test/strict.txt")


    conn = SSHCisco()
    conn.connect("192.168.43.32", 22, username="cisco", password="cisco", timeout=5)
    if conn.isConnected():
        config = conn.readConfig()

    parser = StrictMatchingParser(config, target, verbose)
    parser.parse()