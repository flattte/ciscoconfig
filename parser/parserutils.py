from io import TextIOWrapper
from typing import List, Tuple
import os
import sys
import ipaddress
import argparse

def is_ip_valid(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except:
        return False

def tokenize(config: TextIOWrapper) -> List[List[str]]:
    tokens: List[List] = []
    token: List = []
    for line in filter(None,config.read().splitlines()):
        if '!' in line:
            if token:
                tokens.append(token)
            token = []
        else:
            token.append(line.strip("\t "))
    return tokens


def yieldToken(token: list[list[str]]):
    yield token[1][1]
    for t in token[1][0]:
        yield t


def printToken(token, color="white") -> None:
    if os.name == "nt":
        os.system("color")
    g = yieldToken(token)
    print("Query:")
    print(next(g))
    print("Body:")
    [print(next(g))
     for _ in range(len(token[1][0]))]
    print()


def open_files(path1, path2) -> Tuple[TextIOWrapper, TextIOWrapper]:
    assert type(
        path1) is str, "Enter a -s flag followed by config path to config file."
    assert type(
        path2) is str, "Enter a -t flag followed by config path to config file."
    try:
        file1 = open(path1, 'r')
    except Exception as e:
        exit(
            f"Exception {e.__class__} occurred while opening {path1}. \n Enter a valid path to a file that exists")

    try:
        file2 = open(path2, 'r')
    except Exception as e:
        exit(
            f"Exception {e.__class__} occurred while opening {path2}. \n Enter a valid path to a file that exists")

    return file1, file2

def parse_args(args) -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(description="main gui for ciscoconfig",
                            usage=f"{sys.executable} {sys.argv[0]} -f <path to config file> -u <ssh username> -p <ssh password> -e <privileged exec mode password> -r <rows> -c <columns>")
    arg_parser.add_argument('-f', dest='config_file',
                            help='path to config file.', required=True)
    arg_parser.add_argument('-u', dest='username', help='ssh username', required=True)
    arg_parser.add_argument('-p', dest='password', help='ssh password', required=True)
    arg_parser.add_argument('-e', dest='priv_exec_mode',
                            help='password for privileged exec mode', required=True)
    arg_parser.add_argument('-r', dest='rows', help='number of rows', required=True)
    arg_parser.add_argument('-c', dest='columns', help='number of columns', required=True)
    args = arg_parser.parse_args(args)
    return args