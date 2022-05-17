import os
import termcolor


def tokenizeConfig(config) -> list():
    token, tokens = [], []
    for line in config.read().splitlines():
        if '!' in line:
            if token:
                tokens.append(token)
            token = []
        else:
            token.append(line.strip("\t ").strip(" "))

    return tokens


def tokenizeTarget(target) -> list():
    token, tokens = [], []
    for line in target.read().splitlines():
        if '!' in line:
            if token:
                tokens.append(token)
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
    [print(termcolor.colored(f"    {next(g)}", color))
     for _ in range(len(token[1][0]))]
    print()


def open_files(path1, path2):
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
